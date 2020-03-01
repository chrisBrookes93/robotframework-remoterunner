import os
import base64
from rfremoterunner.utils import read_file_from_disk, normalize_xmlrpc_address
try:
    # Python 2
    from xmlrpclib import ServerProxy
    from xmlrpclib import Binary
except ImportError:
    # Python 3
    from xmlrpc.client import ServerProxy, Binary


DEFAULT_PORT = 1471
ROBOT_FILE_EXT = ('robot', 'txt', 'html')


class RemoteFrameworkClient:

    def __init__(self, address):
        """
        Constructor for RemoteFrameworkServer

        :param address: Hostname/IP of the server with optional :Port
        :type address: str
        """
        self._address = normalize_xmlrpc_address(address, DEFAULT_PORT)
        self._client = ServerProxy(self._address)

    def execute_run(self, suite_list, robot_arg_dict):
        """
        Sources a series of test suites and then makes the RPC call to the
        slave to execute the robot run.

        :param suite_list: List of paths to test suites or directories containing test suites
        :type suite_list: list
        :param robot_arg_dict: Dictionary of arguments to pass to robot.run
        :type robot_arg_dict: dict

        :return: Dictionary containing stdout/err, log.html, output.xml & report.html
        :rtype: dict
        """
        # A user may have specified directory(s) amongst paths to suites, so parse and retrieve them all
        complete_ts_dict = self._source_all_test_suites(suite_list)

        if not complete_ts_dict:
            raise Exception('Failed to find any test suites')

        # Make the RPC
        response = self._client.execute_robot_run(complete_ts_dict, robot_arg_dict)

        return response

    @staticmethod
    def _source_all_test_suites(suite_list):
        """
        Iterates a list of paths to test suites or directories containing test suites, reads them from disk and returns
        their contents a dictionary of file contents

        :param suite_list: List of paths to suites to read or directories containing suites to read
        :type suite_list: list

        :return: Dictionary of test suites, the key being the suite name
        :rtype: dict
        """
        ret_val = {}

        for suite in suite_list:
            file_path, file_ext = os.path.splitext(suite)
            if file_ext:
                if os.path.exists(suite):
                    suite_contents = read_file_from_disk(suite)
                    filename = os.path.basename(suite)
                    ret_val[filename] = Binary(suite_contents)
                else:
                    print('{} does not exist, skipping'.format(suite))
            else:
                suite_dict = RemoteFrameworkClient._fetch_suites_in_directory(suite)
                ret_val.update(suite_dict)

        return ret_val

    @staticmethod
    def _fetch_suites_in_directory(directory):
        """
        Iterates a directory and returns a list of paths to robot test suites. At this stage we can't say for sure
        that its a test suite but we return anything that has the extension of: robot, html, txt

        :param directory: Directory to iterate
        :type directory: str

        :return: Dict of test suite file paths
        :rtype: dict
        """
        ret_val = {}

        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            print('Directory {0} does not exist, skipping'.format(directory))
        else:
            for dir_item in os.listdir(directory):
                if dir_item.endswith(ROBOT_FILE_EXT):
                    full_path = os.path.join(directory, dir_item)
                    suite_name = os.path.basename(dir_item)
                    suite_data = read_file_from_disk(full_path)
                    ret_val[suite_name] = Binary(suite_data)
        return ret_val
