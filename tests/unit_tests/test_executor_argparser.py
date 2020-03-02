import unittest
import os
import tempfile
from rfremoterunner.executor_argparser import ExecutorArgumentParser


class TestExecutorArgumentParser(unittest.TestCase):

    def setUp(self):
        self.curr_dir = os.path.abspath(os.path.dirname(__file__))
        self.suite_dir = os.path.join(self.curr_dir, '..', 'integration_tests', 'resources')
        self.temp_cwd = os.getcwd()
        os.chdir(self.curr_dir)

    def tearDown(self):
        os.chdir(self.temp_cwd)

    def test_get_log_html_output_location_default(self):
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        expected_val = os.path.abspath(os.path.join(self.curr_dir, 'remote_log.html'))
        self.assertEqual(expected_val, actual_val)

    def test_get_log_html_output_location_outputdir_specified(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_log.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_log_html_output_location_log_specified_relative(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--log', 'test_results/log.html']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'test_results', 'log.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_log_html_output_location_log_specified_absolute(self):
        temp_dir = tempfile.gettempdir()
        expected_val = os.path.abspath(os.path.join(temp_dir, 'test_results', 'log.html'))
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--log', expected_val]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        self.assertEqual(expected_val, actual_val)

    def test_get_report_html_output_location_default(self):
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        expected_val = os.path.join(self.curr_dir, 'remote_report.html')
        self.assertEqual(expected_val, actual_val)

    def test_get_report_html_output_location_outputdir_specified(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_report.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_report_html_output_location_log_specified_relative(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--report', 'test_results/report.html']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'test_results', 'report.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_report_html_output_location_log_specified_absolute(self):
        temp_dir = tempfile.gettempdir()
        expected_val = os.path.abspath(os.path.join(temp_dir, 'test_results', 'report.html'))
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--report', expected_val]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        self.assertEqual(expected_val, actual_val)

    def test_get_output_xml_output_location_default(self):
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        expected_val = os.path.join(self.curr_dir, 'remote_output.xml')
        self.assertEqual(expected_val, actual_val)

    def test_get_output_xml_output_location_outputdir_specified(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_output.xml')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_output_xml_output_location_log_specified_relative(self):
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--output', 'test_results/output.xml']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'test_results', 'output.xml')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_output_xml_output_location_log_specified_absolute(self):
        temp_dir = tempfile.gettempdir()
        expected_val = os.path.abspath(os.path.join(temp_dir, 'test_results', 'output.xml'))
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../',
                      '--output', expected_val]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        self.assertEqual(expected_val, actual_val)
