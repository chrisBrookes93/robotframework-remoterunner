from io import open
from mock import patch, MagicMock
import os
from robot.running import TestSuiteBuilder
import six.moves.xmlrpc_client as xmlrpc_client
import unittest

from rfremoterunner.rf_client import RemoteFrameworkClient


class TestRemoteFrameworkClient(unittest.TestCase):

    def setUp(self):

        self.resource_dir = os.path.join(os.path.dirname(__file__), 'rf_client_test_resources')
        builder = TestSuiteBuilder()
        parent_suite = builder.build(self.resource_dir)
        self.ts1 = parent_suite.suites[1]
        self.test_obj = RemoteFrameworkClient('127.0.0.1')

    def assert_file_contents_is_equal(self, file_path, expected_file_data):
        """
        Helper function to verify the contents of a file

        :param file_path: Path to the file to verify
        :type file_path: str
        :param expected_file_data: Expected file data
        :type expected_file_data: str
        """
        if not os.path.exists(file_path):
            raise Exception('File does not exist:' + file_path)

        with open(file_path, 'r', encoding='utf-8') as fp:
            file_data = fp.read()
        self.assertEqual(expected_file_data, file_data)

    def test_execute_run_single_dir(self):
        """
        Test that execute_run() correctly collects the test suites and resources when given a single directory
        """
        mock_server_proxy = MagicMock(spec=xmlrpc_client.ServerProxy)
        mock_server_proxy.execute_robot_run = lambda suites, deps, robot_args, debug: None

        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, 'txt:robot', None, {})

            expected_dependencies = ['Lib1.py', 'Lib2.py', 'Lib3.py', 'Res1.robot', 'Res2.robot', 'Res3.robot']
            expected_test_suites = ['TS1.robot', 'S-TS2.robot', 'S-TS3.txt', 'S-TS4.robot', 'T-TS5.robot', 'T-TS6.txt']
            self.assertListEqual(sorted(expected_dependencies), sorted(test_obj._dependencies.keys()))
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))

    def test_execute_run_correct_suite_filtering(self):
        """
        Test that execute_run() correctly collects the test suites and resources when given a suite filter
        """
        mock_server_proxy = MagicMock(spec=xmlrpc_client.ServerProxy)
        mock_server_proxy.execute_robot_run = lambda suites, deps, robot_args, debug: None

        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, 'txt:robot', ['S-*'], {})
            expected_test_suites = ['S-TS2.robot', 'S-TS3.txt', 'S-TS4.robot']
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))

    def test_execute_run_correct_suite_extension(self):
        """
        Test that execute_run() correctly collects the test suites and resources when given a suite extension filter.
        """
        mock_server_proxy = MagicMock(spec=xmlrpc_client.ServerProxy)
        mock_server_proxy.execute_robot_run = lambda suites, deps, robot_args, debug: None

        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, 'txt', None, {})
            expected_test_suites = ['S-TS3.txt', 'T-TS6.txt']
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))

    # def test_create_test_suite_builder_extensions_provided(self):
    #     """
    #     Test that _create_test_suite_builder() correctly constructs the builder when extensions are provided
    #     """
    #     self.assertFalse(True)
    #
    # def test_create_test_suite_builder_no_extension_provided(self):
    #     """
    #     Test that _create_test_suite_builder() correctly constructs the builder when extensions are not provided
    #     """
    #     self.assertFalse(True)
    #
    # def test_create_test_suite_builder_pre_three_dot_two(self):
    #     """
    #     Test that _create_test_suite_builder() correctly constructs the builder when the API is pre robotframework 3.2
    #     """
    #     self.assertFalse(True)
    #
    # def test_process_test_suite(self):
    #     """
    #     Test that _process_test_suite() parses a test suite and returns the correct dictionary
    #     """
    #     self.assertFalse(True)
