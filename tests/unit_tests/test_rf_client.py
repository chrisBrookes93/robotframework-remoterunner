import unittest
from mock import patch, MagicMock
from rfremoterunner.rf_client import RemoteFrameworkClient
try:
    # Python 2
    from xmlrpclib import Binary
except ImportError:
    # Python3
    from xmlrpc.client import Binary


class TestRemoteFrameworkClient(unittest.TestCase):

    def test_execute_run_no_test_suites_to_exec(self):
        rfc = RemoteFrameworkClient('127.0.0.1')

        with patch('rfremoterunner.rf_client.RemoteFrameworkClient._source_all_test_suites', return_value={}):
            self.assertRaisesRegexp(Exception,
                                   'Failed to find any test suites',
                                   rfc.execute_run,
                                   ['./Suite1.robot'],
                                   {'loglevel': 'TRACE'})

    def test_execute_run_correct_case(self):
        stdouterr = b'StdOut & StdErr'
        mocked_results = {'std_out_err': Binary(stdouterr),
                          'result_html': Binary(b'result'),
                          'output_xml': Binary(b'output'),
                          'report_html': Binary(b'report')}
        suite_dict = {'Suite1.robot': 'blah', 'Suite2.robot': 'blah'}
        with patch('rfremoterunner.rf_client.RemoteFrameworkClient._source_all_test_suites', return_value=suite_dict), \
             patch('rfremoterunner.rf_client.ServerProxy', return_value=MagicMock()) as patched_server_proxy:

            patched_server_proxy.return_value.execute_robot_run.return_value = mocked_results
            rfc = RemoteFrameworkClient('127.0.0.1')
            actual_val = rfc.execute_run(['Suite1.robot'], {'loglevel': 'TRACE'})
            self.assertListEqual(sorted(mocked_results.keys()), sorted(actual_val.keys()))
            self.assertEqual(stdouterr, actual_val['std_out_err'])

    def test_source_all_test_suites_path_to_suite(self):
        expected_suite_name = 'Suite1.robot'
        expected_file_contents = b'file data'
        with patch('os.path.exists', return_value=True), \
             patch('rfremoterunner.rf_client.read_file_from_disk', return_value=expected_file_contents):

            actual_val = RemoteFrameworkClient._source_all_test_suites([expected_suite_name])
            self.assertIn(expected_suite_name, actual_val)
            self.assertEqual(expected_file_contents, actual_val[expected_suite_name])

    def test_source_all_test_suites_path_to_dir(self):
        expected_dict = {'Suite1.robot': 'blah', 'Suite2.robot': 'blah'}
        with patch('rfremoterunner.rf_client.RemoteFrameworkClient._fetch_suites_in_directory', return_value=expected_dict):
            actual_val = RemoteFrameworkClient._source_all_test_suites(['directory_name'])
            self.assertListEqual(sorted(expected_dict.keys()), sorted(actual_val.keys()))

    def test_fetch_suites_in_directory_correct_case(self):
        expected_file_contents = b'file data'
        expected_suite_names = ['Suite1.robot', 'Suite2.robot', 'Suite3.txt', 'Suite4.html']
        with patch('os.listdir', return_value=expected_suite_names + ['NotASuite.dat']), \
             patch('os.path.exists', return_value=True), \
             patch('rfremoterunner.rf_client.read_file_from_disk', return_value=expected_file_contents):
            actual_val = RemoteFrameworkClient._fetch_suites_in_directory('directory_name')
            self.assertListEqual(sorted(actual_val.keys()), sorted(expected_suite_names))
