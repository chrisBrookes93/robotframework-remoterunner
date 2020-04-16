import unittest
import os
from io import open
from robot.model.imports import Import
from mock import patch, MagicMock
from rfremoterunner.rf_client import RemoteFrameworkClient
from robot.running import TestSuiteBuilder


class TestRemoteFrameworkClient(unittest.TestCase):

    def setUp(self):

        self.resource_dir = os.path.join(os.path.dirname(__file__), 'rf_client_test_resources')
        builder = TestSuiteBuilder()
        parent_suite = builder.build(self.resource_dir)
        self.ts1 = parent_suite.suites[1]
        self.test_obj = RemoteFrameworkClient('127.0.0.1')

    def file_contents_is_equal(self, file_path, expected_file_data):
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

    def test_process_test_suite(self):

        def mock_process_dependency(dep):
            # Modify in some way so that we know we have the modified references is in the suite file data
            dep.name = os.path.basename(dep.name)

        with patch('rfremoterunner.rf_client.RemoteFrameworkClient._process_dependency',
                   side_effect=mock_process_dependency) as patched_process_dependency:
            result = self.test_obj._process_test_suite(self.ts1)
            suite_data = result.get('suite_data')
            self.assertEqual('Rf Client Test Resources', result.get('path'))

            # Check that dependency are uppercase to check that they've been updated
            self.assertRegexpMatches(suite_data, 'Resource[\\s]+Res1\\.robot')
            self.assertRegexpMatches(suite_data, 'Library[\\s]+Lib1\\.py')
            self.assertRegexpMatches(suite_data, 'Library[\\s]+Lib3\\.py')
            patched_process_dependency.assert_any_call(self.ts1.resource.imports[0])
            patched_process_dependency.assert_any_call(self.ts1.resource.imports[1])
            patched_process_dependency.assert_any_call(self.ts1.resource.imports[2])

    def test_process_dependency_resource(self):
        imp = Import('Resource', './primary_dependencies/Res1.robot', source=self.ts1.source)
        self.test_obj._process_dependency(imp)
        # res1 (Res1.robot) has a dependency on Res2.robot & Lib3.py. Res2.robot has a dependency on Res3.robot & Lib3.py
        expected_dependencies = ['Res1.robot', 'Res2.robot', 'Res3.robot', 'Lib3.py']
        self.assertListEqual(sorted(expected_dependencies), sorted(self.test_obj._dependencies.keys()))
        # Check that the paths to dependencies have been updated
        self.assertRegexpMatches(self.test_obj._dependencies['Res3.robot'], 'Library[\\s]+Lib3\\.py')
        self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Library[\\s]+Lib3\\.py')
        self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Resource[\\s]+Res3\\.robot')
        self.assertRegexpMatches(self.test_obj._dependencies['Res1.robot'], 'Resource[\\s]+Res2\\.robot')
        self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Library[\\s]+Lib3\\.py')

    def test_process_dependency_library(self):
        imp = Import('Library', './primary_dependencies/Lib1.py', source=self.ts1.source)
        self.test_obj._process_dependency(imp)
        self.assertIn('Lib1.py', self.test_obj._dependencies)
        ts1_lib1_py_path = os.path.join(self.resource_dir, 'primary_dependencies', 'Lib1.py')
        self.file_contents_is_equal(ts1_lib1_py_path, self.test_obj._dependencies['Lib1.py'])

    def test_execute_run_single_dir(self):
        mock_server_proxy = MagicMock()
        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, None, None, {})

            expected_dependencies = ['Lib1.py', 'Lib2.py', 'Lib3.py', 'Res1.robot', 'Res2.robot', 'Res3.robot']
            expected_test_suites = ['TS1.robot', 'S-TS2.robot', 'S-TS3.txt', 'S-TS4.robot', 'T-TS5.robot', 'T-TS6.txt']
            self.assertListEqual(sorted(expected_dependencies), sorted(test_obj._dependencies.keys()))
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))

    def test_execute_run_correct_suite_filtering(self):
        mock_server_proxy = MagicMock()
        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, None, ['S-*'], {})
            expected_test_suites = ['S-TS2.robot', 'S-TS3.txt', 'S-TS4.robot']
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))

    def test_execute_run_correct_suite_extension(self):
        mock_server_proxy = MagicMock()
        with patch('rfremoterunner.rf_client.xmlrpc_client.ServerProxy', return_value=mock_server_proxy):
            # In order to mock the server we need to initialize this here, so the one created in the setup cannot be
            # used
            test_obj = RemoteFrameworkClient('127.0.0.1')
            suite_list = [self.resource_dir]
            test_obj.execute_run(suite_list, 'txt', None, {})
            expected_test_suites = ['S-TS3.txt', 'T-TS6.txt']
            self.assertListEqual(sorted(expected_test_suites), sorted(test_obj._suites.keys()))
