from io import open
import os
import unittest
import six.moves.xmlrpc_client as xmlrpc_client
from mock import patch, MagicMock
from robot.api import TestSuiteBuilder

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

        with open(file_path, 'r', encoding='utf-8') as file_handle:
            file_data = file_handle.read()
        self.assertEqual(expected_file_data, file_data)

    def test_execute_run_single_dir(self):
        """
        Test that execute_run() correctly collects the test suites and resources when given a single directory
        """
        expected_deps = {
            'Lib1.py': "\n\ndef Keyword_43543543():\n    print('Keyword 1')",
            'Lib3.py': "\n\ndef Keyword_343534():\n    print('Keyword 1')",
            'Res3.robot': '*** Settings ***\nLibrary    Lib3.py\n\n*** Keywords ***\nK1\n    Log    K1\n',
            'Lib2.py': "\n\ndef Keyword_34543534():\n    print('Keyword 1')",
            'Res2.robot': '*** Settings ***\nResource    Res3.robot\nLibrary     Lib3.py\n\n*** Keywords ***\nK1\n '
                          '   Log    K1\n',
            'Res1.robot': '*** Settings ***\nResource    Res2.robot\nLibrary    Lib3.py\n\n*** Keywords ***\nK1\n  '
                          '  Log    K1\n'
        }

        expected_suites = {
            'S-TS2.robot': {
                'path': 'Rf Client Test Resources/Secondary Test Suites',
                'suite_data': '*** Settings ***\nLibrary           Lib1.py\n\n*** Test Cases ***\nS_TS2.1\n    Log  '
                              '  1\n'
            },
            'S-TS3.txt': {
                'path': 'Rf Client Test Resources/Secondary Test Suites',
                'suite_data': '*** Settings ***\nResource          Res3.robot\nLibrary           Lib2.py\n\n*** Test '
                              'Cases ***\nS_TS3.1\n    Log    1\n'
            },
            'S-TS4.robot': {
                'path': 'Rf Client Test Resources/Secondary Test Suites',
                'suite_data': '*** Settings ***\n\n*** Test Cases ***\nS_TS4.1\n    Log    1\n'
            },
            'T-TS5.robot': {
                'path': 'Rf Client Test Resources/Secondary Test Suites/Tertiary Test Suites',
                'suite_data': '*** Settings ***\nLibrary           Lib2.py\n\n*** Test Cases ***\nT_TS5.1\n    Log  '
                              '  1\n'
            },
            'T-TS6.txt': {
                'path': 'Rf Client Test Resources/Secondary Test Suites/Tertiary Test Suites',
                'suite_data': '*** Settings ***\nLibrary           Lib3.py\n\n*** Test Cases ***\nT_TS6.1\n    Log    '
                              '1\n'
            }, 'TS1.robot': {
                'path': 'Rf Client Test Resources',
                'suite_data': '*** Settings ***\nResource          Res1.robot\nLibrary           Lib1.py\nLibrary     '
                              '      Lib3.py\n\n*** Test Cases ***\nTS1.1\n    Log    1\n'
            }
        }
        expected_args = {'include': 'Tag1'}

        mock_server_proxy = MagicMock(spec=xmlrpc_client.ServerProxy)
        mock_server_proxy.execute_robot_run = MagicMock()

        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, 'txt:robot', None, expected_args)
            mock_server_proxy.execute_robot_run.assert_called_once_with(expected_suites,
                                                                        expected_deps,
                                                                        expected_args,
                                                                        False)

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

    def test_create_test_suite_builder_extensions_provided(self):
        """
        Test that _create_test_suite_builder() correctly constructs the builder when extensions are provided
        """
        # Intentionally not using autospec=True here as the constructor definition is different across versions
        with patch('rfremoterunner.rf_client.TestSuiteBuilder') as mock_suite_builder:

            suite_list = [self.resource_dir]
            extension = 'txt:robot'
            RemoteFrameworkClient._create_test_suite_builder(suite_list, extension)
            mock_suite_builder.assert_any_call(suite_list, included_extensions=extension.split(':'))

    def test_create_test_suite_builder_no_extension_provided(self):
        """
        Test that _create_test_suite_builder() correctly constructs the builder when extensions are not provided
        """
        # Intentionally not using autospec=True here as the constructor definition is different across versions
        with patch('rfremoterunner.rf_client.TestSuiteBuilder') as mock_suite_builder:

            suite_list = [self.resource_dir]
            extension = None
            RemoteFrameworkClient._create_test_suite_builder(suite_list, extension)
            mock_suite_builder.assert_any_call(suite_list, included_extensions=['robot'])

    def test_create_test_suite_builder_pre_three_dot_two(self):
        """
        Test that _create_test_suite_builder() correctly constructs the builder when the API is pre robotframework 3.2
        """
        # Intentionally not using autospec=True here as the constructor definition is different across versions
        with patch('rfremoterunner.rf_client.TestSuiteBuilder') as mock_suite_builder:
            mock_suite_builder.side_effect = TypeError, None

            suite_list = [self.resource_dir]
            extension = 'txt:robot'
            RemoteFrameworkClient._create_test_suite_builder(suite_list, extension)
            mock_suite_builder.assert_any_call(suite_list, included_extensions=extension.split(':'))
            mock_suite_builder.assert_any_call(suite_list, extension=extension)
