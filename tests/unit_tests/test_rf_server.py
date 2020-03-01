import unittest
from rfremoterunner.rf_server import RobotFrameworkServer
from mock import patch


class TestRemoteFrameworkServer(unittest.TestCase):

    def setUp(self):
        self.test_obj = RobotFrameworkServer()

    def tearDown(self):
        self.test_obj._server.server_close()

    def test_execute_robot_run_correct_case(self):
        with patch('rfremoterunner.rf_server.RobotFrameworkServer._write_remote_suites_to_disk',
                   return_value='directory'), \
             patch('rfremoterunner.rf_server.run'), \
             patch('rfremoterunner.rf_server.RobotFrameworkServer._read_robot_artifacts_from_disk',
                   return_value=(b'blah', b'blah', b'blah')), \
             patch('rfremoterunner.rf_server.shutil.rmtree') as patched_rmtree, \
             patch('os.chdir'):

            actual_val = self.test_obj.execute_robot_run({'Suite1.robot':'blah'}, {'loglevel': 'TRACE'})
            patched_rmtree.assert_called_once_with('directory')


    def test_write_remote_suites_to_disk_correct_case(self):
         self.assertTrue(False)

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
