import tempfile
import os
import shutil
import sys
import logging
import six.moves.xmlrpc_client as xmlrpc_client
import six.moves.xmlrpc_server as xmlrpc_server
from six import StringIO
from robot.run import run
from rfremoterunner.utils import write_file_to_disk, read_file_from_disk

logger = logging.getLogger('rfremoterunner.slave')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(message)s'))
out_hdlr.setLevel(logging.DEBUG)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)

DEFAULT_ADDRESS = '0.0.0.0'
DEFAULT_PORT = 1471


class RobotFrameworkServer:

    # Executable RPC functions
    EXECUTE_FUNC = 'execute_robot_run'

    def __init__(self, address=DEFAULT_ADDRESS, port=DEFAULT_PORT, debug=False):
        """
        Constructor for RobotFrameworkServer

        :param address: Address to bind to. Default is localhost
        :type address: str
        :param port: Port to listen on. Default is 1471
        :type port: int
        :param debug: Run in debug mode. This changes the logging level and does not cleanup the workspace
        :type debug: bool
        """
        self._address = address
        self._port = port
        self._server = xmlrpc_server.SimpleXMLRPCServer((address, int(port)), encoding='utf-8')
        self._server.register_function(RobotFrameworkServer.execute_robot_run, self.EXECUTE_FUNC)
        logging_level = logging.DEBUG if debug else logging.INFO
        logger.setLevel(logging_level)

    def serve(self):
        """
        Blocking call to wait for XML-RPC connections
        """
        logger.info('Listening on {}:{}'.format(self._address, self._port))
        self._server.serve_forever()

    @staticmethod
    def execute_robot_run(test_suites, dependencies, robot_args, debug=False):
        """
        Callback that is invoked when a request to execute a robot run is made

        :param test_suites: Dictionary of suites to execute
        :type test_suites: dict
        :param dependencies: Dictionary of files that the test suites are dependant on
        :type dependencies: dict
        :param robot_args: Dictionary of arguments to pass to robot.run()
        :type robot_args: dict
        :param debug: Run in debug mode. This changes the logging level and does not cleanup the workspace
        :type debug: bool

        :return: Dictionary containing test results and artifacts
        :rtype: dict
        """
        workspace_dir = None
        std_out_err = None
        old_cwd = None
        try:
            old_log_level = logger.level
            if debug:
                logger.setLevel(logging.DEBUG)

            # Save all suites & dependencies to disk
            workspace_dir = RobotFrameworkServer._create_workspace(test_suites, dependencies)

            # Change the CWD to the workspace
            old_cwd = os.getcwd()
            os.chdir(workspace_dir)
            sys.path.append(workspace_dir)

            # Execute the robot run
            std_out_err = StringIO()
            logger.debug('Beginning Robot Run.')
            logger.debug('Robot Run Args: ' + str(robot_args))
            ret_code = run('.',
                           stdout=std_out_err,
                           stderr=std_out_err,
                           outputdir=workspace_dir,
                           name='Root',
                           **robot_args)
            logger.debug('Robot Run finished')
            os.chdir(old_cwd)

            # Read the test artifacts from disk
            output_xml, log_html, report_html = RobotFrameworkServer._read_robot_artifacts_from_disk(workspace_dir)

            ret_val = {'std_out_err': xmlrpc_client.Binary(std_out_err.getvalue().encode('utf-8')),
                       'output_xml': xmlrpc_client.Binary(output_xml.encode('utf-8')),
                       'log_html': xmlrpc_client.Binary(log_html.encode('utf-8')),
                       'report_html': xmlrpc_client.Binary(report_html.encode('utf-8')),
                       'ret_code': ret_code}
        except Exception as e:
            # Log here because the RPC framework doesn't give the client a full stacktrace
            logging.error(e)
            raise
        finally:
            if old_cwd:
                os.chdir(old_cwd)

            if std_out_err:
                std_out_err.close()

            if workspace_dir and not debug:
                shutil.rmtree(workspace_dir)

        logger.debug('End of RPC function')
        # Revert the logger back to its original level
        logger.setLevel(old_log_level)
        return ret_val

    @staticmethod
    def _create_workspace(test_suites, dependencies):
        """
        Create a directory in the temporary directory and write all test suites & dependencies to disk

        :param test_suites: Dictionary of test suites
        :type test_suites: dict
        :param test_suites: Dictionary of files the test suites are dependent on
        :type test_suites: dict

        :return: An absolute path to the directory created
        :rtype: str
        """
        workspace_dir = tempfile.mkdtemp()
        logger.debug('Created workspace at: {}'.format(workspace_dir))

        for suite_name, suite in test_suites.items():
            full_dir = os.path.join(workspace_dir, suite.get('path'))
            if not os.path.exists(full_dir):
                os.makedirs(full_dir)
            full_path = os.path.join(full_dir, suite_name)
            logger.debug('Writing suite to disk: {}'.format(full_path))
            write_file_to_disk(full_path, suite.get('suite_data'))

        for dep_name, dep_data in dependencies.items():
            full_path = os.path.join(workspace_dir, dep_name)
            logger.debug('Writing dependency to disk: {}'.format(full_path))
            write_file_to_disk(full_path, dep_data)

        return workspace_dir

    @staticmethod
    def _read_robot_artifacts_from_disk(workspace_dir):
        """
        Read and return the contents of the output xml, log html and report html files generated by robot.

        :param workspace_dir: Directory containing the test artifacts
        :type workspace_dir: str

        :return: File data (output xml, log html, report html)
        :rtype: tuple
        """
        log_html = ''
        log_html_path = os.path.join(workspace_dir, 'log.html')
        if os.path.exists(log_html_path):
            logger.debug('Reading log.html file off disk from: {}'.format(log_html_path))
            log_html = read_file_from_disk(os.path.join(workspace_dir, 'log.html'))

        report_html = ''
        report_html_path = os.path.join(workspace_dir, 'report.html')
        if os.path.exists(report_html_path):
            logger.debug('Reading report.html file off disk from: {}'.format(report_html_path))
            report_html = read_file_from_disk(report_html_path)

        output_xml = ''
        output_xml_path = os.path.join(workspace_dir, 'output.xml')
        if os.path.exists(output_xml_path):
            logger.debug('Reading output.xml file off disk from: {}'.format(output_xml_path))
            output_xml = read_file_from_disk(output_xml_path)

        return output_xml, log_html, report_html
