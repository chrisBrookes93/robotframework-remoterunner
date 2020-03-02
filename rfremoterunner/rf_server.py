import tempfile
import os
import shutil
import six
from robot.run import run
from rfremoterunner.utils import generate_temporary_directory_name, write_file_to_disk, read_file_from_disk
try:
    # Python 2
    from StringIO import StringIO
    from SimpleXMLRPCServer import SimpleXMLRPCServer
    from xmlrpclib import Binary
except ImportError:
    # Python3
    from xmlrpc.server import SimpleXMLRPCServer
    from xmlrpc.client import Binary
    from io import StringIO

if six.PY3:
    unicode = str

DEFAULT_PORT = 1471


class RobotFrameworkServer:

    # Executable RPC functions
    EXECUTE_FUNC = 'execute_robot_run'

    def __init__(self, address='127.0.0.1', port=DEFAULT_PORT, debug=False):
        """
        Constructor for RobotFrameworkServer

        :param address: Address to bind to. Default is localhost
        :type address: str
        :param port: Port to listen on. Default is 1471
        :type port: int
        :param debug: Start in debug mode
        :type: bool
        """
        self._address = address
        self._port = port
        self._debug = debug
        self._server = SimpleXMLRPCServer((address, int(port)))
        self._server.register_function(RobotFrameworkServer.execute_robot_run, self.EXECUTE_FUNC)

    def serve(self):
        """
        Blocking call to wait for XML-RPC connections
        """
        print('Listening on {}:{}'.format(self._address, self._port))
        self._server.serve_forever()

    @staticmethod
    def execute_robot_run( suite_dict, robot_args):
        """
        Callback that is invoked when a request to execute a robot run is made

        :param suite_dict: Dictionary of suites to execute
        :type suite_dict: dict
        :param robot_args: Dictionary of arguments to pass to robot.run()
        :type robot_args: dict

        :return: Dictionary containing test results and artifacts
        :rtype: dict
        """
        workspace_dir = None
        try:
            # Save all suites to disk
            workspace_dir = RobotFrameworkServer._write_remote_suites_to_disk(suite_dict)

            # Change the CWD
            old_cwd = os.getcwd()
            os.chdir(workspace_dir)

            # Execute the robot run
            suite_names = suite_dict.keys()
            std_out_err = StringIO()
            run(stdout=std_out_err,
                stderr=std_out_err,
                outputdir=workspace_dir,
                *suite_names,
                **robot_args)
            os.chdir(old_cwd)

            stdout_err_val = std_out_err.getvalue()
            # An annoying encoding issue I haven't worked out yet
            if six.PY2:
                stdout_err_val = Binary(bytes(stdout_err_val))
            else:
                stdout_err_val = Binary(stdout_err_val.encode())

            std_out_err.close()
            # Read the test artifacts from disk
            output_xml, log_html, report_html = RobotFrameworkServer._read_robot_artifacts_from_disk(workspace_dir)
        finally:
            if workspace_dir:
                shutil.rmtree(workspace_dir)

        return {'std_out_err': stdout_err_val,
                'output_xml': Binary(output_xml),
                'log_html': Binary(log_html),
                'report_html': Binary(report_html)}

    @staticmethod
    def _write_remote_suites_to_disk(suites):
        """
        Create a directory in the temporary directory and write all test suites to disk

        :param suites: Suites to save
        :type suites: dict

        :return: An absolute path to the directory created
        :rtype: str
        """
        workspace_dir = os.path.abspath(os.path.expandvars(os.path.join(tempfile.gettempdir(),
                                                                        generate_temporary_directory_name())))
        os.mkdir(workspace_dir)

        for suite_name, suite_data in suites.items():
            full_path = os.path.join(workspace_dir, suite_name)
            write_file_to_disk(full_path, suite_data.data)

        return workspace_dir

    @staticmethod
    def _read_robot_artifacts_from_disk(workspace_dir):
        """
        Read and return the contents of output.xml, log.html, report.html

        :param workspace_dir: Directory containing the test artifacts
        :type workspace_dir: str

        :return: output_xml, log.html, report.html
        :rtype: tuple
        """
        log_html = ''
        log_html_path = os.path.join(workspace_dir, 'log.html')
        if os.path.exists(log_html_path):
            log_html = read_file_from_disk(os.path.join(workspace_dir, 'log.html'))

        report_html = ''
        report_html_path = os.path.join(workspace_dir, 'report.html')
        if os.path.exists(report_html_path):
            report_html = read_file_from_disk(report_html_path)

        output_xml = ''
        output_xml_path = os.path.join(workspace_dir, 'output.xml')
        if os.path.exists(output_xml_path):
            output_xml = read_file_from_disk(output_xml_path)

        return output_xml, log_html, report_html
