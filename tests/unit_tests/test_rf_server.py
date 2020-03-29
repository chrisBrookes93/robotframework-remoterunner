import unittest
import os
import shutil
from io import open
from mock import patch
from rfremoterunner.rf_server import RobotFrameworkServer


class TestRemoteFrameworkServer(unittest.TestCase):

    def setUp(self):
        self.test_obj = RobotFrameworkServer()
        self.to_delete = None

    def tearDown(self):
        self.test_obj._server.server_close()
        if self.to_delete:
            shutil.rmtree(self.to_delete)

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

    def test_create_workspace(self):
        ts_1 = {'path': 'A/B/C/D/E', 'suite_data': 'ts_1' * 10}
        ts_2 = {'path': 'A/B/C/D/E', 'suite_data': 'ts_2' * 10}
        ts_3 = {'path': 'TS3.robot', 'suite_data': 'ts_3' * 10}
        ts_4 = {'path': 'Y/Z/TS3.robot', 'suite_data': 'ts_4' * 10}
        test_suites = {
            'Test Suite1.robot': ts_1,
            'Test Suite2.txt': ts_2,
            'Test_Suite3.robot': ts_3,
            'Test Suite4.robot': ts_4
        }
        dependencies = {
            'dep1.robot': 'dep1.robot' * 10,
            'dep2.robot': 'dep2.robot' * 10,
            'dep3.py': 'dep3.py' * 10
        }

        workspace_dir = RobotFrameworkServer._create_workspace(test_suites, dependencies)
        self.to_delete = workspace_dir
        self.assertTrue(os.path.exists(workspace_dir))

        self.file_contents_is_equal(os.path.join(workspace_dir, ts_1['path'], 'Test Suite1.robot'), ts_1['suite_data'])
        self.file_contents_is_equal(os.path.join(workspace_dir, ts_2['path'], 'Test Suite2.txt'), ts_2['suite_data'])
        self.file_contents_is_equal(os.path.join(workspace_dir, ts_3['path'], 'Test_Suite3.robot'), ts_3['suite_data'])
        self.file_contents_is_equal(os.path.join(workspace_dir, ts_4['path'], 'Test Suite4.robot'), ts_4['suite_data'])

        self.file_contents_is_equal(os.path.join(workspace_dir, 'dep1.robot'), dependencies['dep1.robot'])
        self.file_contents_is_equal(os.path.join(workspace_dir, 'dep2.robot'), dependencies['dep2.robot'])
        self.file_contents_is_equal(os.path.join(workspace_dir, 'dep3.py'), dependencies['dep3.py'])

    def test_execute_robot_run_correct_case(self):
        expected_dict_keys = ['std_out_err', 'output_xml', 'log_html', 'report_html', 'ret_code']
        expected_output_bytes = 'output.xml bytes'
        expected_log_bytes = 'log.html bytes'
        expected_report_bytes = 'report.html bytes'
        robot_artifacts = (expected_output_bytes, expected_log_bytes, expected_report_bytes)
        expected_rc = 123
        with patch('rfremoterunner.rf_server.RobotFrameworkServer._create_workspace', return_value='directory'), \
             patch('rfremoterunner.rf_server.run', return_value=expected_rc), \
             patch('rfremoterunner.rf_server.RobotFrameworkServer._read_robot_artifacts_from_disk',
                   return_value=robot_artifacts), \
             patch('rfremoterunner.rf_server.shutil.rmtree') as patched_rmtree, \
                patch('os.chdir'):
            actual_val = self.test_obj.execute_robot_run({'Suite1.robot': 'blah'}, {}, {'loglevel': 'TRACE'})
            self.assertListEqual(sorted(expected_dict_keys), sorted(list(actual_val.keys())))
            self.assertEqual(expected_output_bytes, actual_val['output_xml'].data.decode('utf-8'))
            self.assertEqual(expected_log_bytes, actual_val['log_html'].data.decode('utf-8'))
            self.assertEqual(expected_report_bytes, actual_val['report_html'].data.decode('utf-8'))
            self.assertEqual(expected_rc, actual_val['ret_code'])

            patched_rmtree.assert_called_once_with('directory')

    def test_read_robot_artifacts_from_disk_files_exist(self):
        expected_file_contents = ['Log HTML Data', 'Report HTML Data', 'Output XML Data']
        with patch('os.path.exists', return_value=True), \
             patch('rfremoterunner.rf_server.read_file_from_disk', side_effect=expected_file_contents):
            output_xml, log_html, report_html = self.test_obj._read_robot_artifacts_from_disk('workspace')
            self.assertEqual(expected_file_contents[0], log_html)
            self.assertEqual(expected_file_contents[1], report_html)
            self.assertEqual(expected_file_contents[2], output_xml)

    def test_read_robot_artifacts_from_disk_files_do_not_exist(self):
        output_xml, log_html, report_html = self.test_obj._read_robot_artifacts_from_disk('%TEMP%/NOT_EXIST/')
        self.assertEqual('', output_xml)
        self.assertEqual('', log_html)
        self.assertEqual('', report_html)
