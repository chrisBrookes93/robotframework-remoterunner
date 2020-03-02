import unittest
from rfremoterunner.rf_server import RobotFrameworkServer
from mock import patch
try:
    # Python 2
    from xmlrpclib import Binary
except ImportError:
    # Python3
    from xmlrpc.client import Binary


class TestRemoteFrameworkServer(unittest.TestCase):

    def setUp(self):
        self.test_obj = RobotFrameworkServer()

    def tearDown(self):
        self.test_obj._server.server_close()

    def test_execute_robot_run_correct_case(self):
        expected_dict_keys = ['std_out_err', 'output_xml', 'log_html', 'report_html']
        expected_output_bytes = b'output.xml bytes'
        expected_log_bytes = b'log.html bytes'
        expected_report_bytes = b'report.html bytes'
        with patch('rfremoterunner.rf_server.RobotFrameworkServer._write_remote_suites_to_disk',
                   return_value='directory'), \
             patch('rfremoterunner.rf_server.run'), \
             patch('rfremoterunner.rf_server.RobotFrameworkServer._read_robot_artifacts_from_disk',
                   return_value=(expected_output_bytes, expected_log_bytes, expected_report_bytes)), \
             patch('rfremoterunner.rf_server.shutil.rmtree') as patched_rmtree, \
             patch('os.chdir'):

            actual_val = self.test_obj.execute_robot_run({'Suite1.robot':'blah'}, {'loglevel': 'TRACE'})
            self.assertListEqual(sorted(expected_dict_keys), sorted(list(actual_val.keys())))
            self.assertEqual(actual_val['output_xml'].data, expected_output_bytes)
            self.assertEqual(actual_val['log_html'].data, expected_log_bytes)
            self.assertEqual(actual_val['report_html'].data, expected_report_bytes)

            patched_rmtree.assert_called_once_with('directory')

    def test_write_remote_suites_to_disk_correct_case(self):
        dummy_workspace_dir = '/a/fake/directory'
        suite_dict = {'Suite1.robot': Binary(b'aaaaa'), 'Suite2.robot': Binary(b'bbbbbb')}

        with patch('os.path.abspath', return_value=dummy_workspace_dir), \
             patch('os.mkdir'), \
             patch('rfremoterunner.rf_server.generate_temporary_directory_name', return_value='randomdir'), \
             patch('tempfile.gettempdir', return_value='temp'), \
             patch('rfremoterunner.rf_server.write_file_to_disk') as patched_write:

            self.test_obj._write_remote_suites_to_disk(suite_dict)
            self.assertEqual(2, patched_write.call_count)

    def test_read_robot_artifacts_from_disk_files_exist(self):
        expected_file_contents = 'file data'
        with patch('os.path.exists', return_value=True):
            with patch('rfremoterunner.rf_server.read_file_from_disk', return_value=expected_file_contents):
                output_xml, log_html, report_html = self.test_obj._read_robot_artifacts_from_disk('%TEMP%/NOT_EXIST/')
                self.assertEqual(expected_file_contents, output_xml)
                self.assertEqual(expected_file_contents, log_html)
                self.assertEqual(expected_file_contents, report_html)

    def test_read_robot_artifacts_from_disk_files_do_not_exist(self):
        output_xml, log_html, report_html = self.test_obj._read_robot_artifacts_from_disk('%TEMP%/NOT_EXIST/')
        self.assertEqual('', output_xml)
        self.assertEqual('', log_html)
        self.assertEqual('', report_html)
