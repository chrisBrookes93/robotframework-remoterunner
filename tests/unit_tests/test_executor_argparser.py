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

    def test_args_set_correctly(self):
        """
        Test that all arguments are set correctly in the ExecutorArgumentParser
        """
        expected_host = '192.168.56.1'
        expected_suites = self.suite_dir
        expected_output_dir = '../../'
        expected_output_xml = './out.xml'
        expected_log_file = './l.html'
        expected_report_file = './r.html'
        expected_extension = 'html:tsv'
        expected_include = 'ts_*'
        expected_exclude = 'nts_*'
        expected_test = 'a.b.c.*'
        expected_suite = 'X.Y:X.Z:Y.A'.split(':')
        expected_log_level = 'DEBUG'

        input_args = [expected_host,
                      expected_suites,
                      '--outputdir', expected_output_dir,
                      '--output', expected_output_xml,
                      '--log', expected_log_file,
                      '--report', expected_report_file,
                      '--debug',
                      '--extension', expected_extension,
                      '--include', expected_include,
                      '--exclude', expected_exclude,
                      '--test', expected_test,
                      '--suite', 'X.Y:X.Z:Y.A',
                      '--loglevel', expected_log_level,
                      ]
        eap = ExecutorArgumentParser(input_args)
        self.assertEqual(eap.host, expected_host)
        self.assertEqual(eap.suites, [expected_suites])
        self.assertEqual(eap.outputdir, expected_output_dir)
        self.assertEqual(eap.output, expected_output_xml)
        self.assertEqual(eap.log, expected_log_file)
        self.assertEqual(eap.report, expected_report_file)
        self.assertTrue(eap.debug)
        self.assertEqual(eap.extension, expected_extension)
        self.assertEqual(eap.include, expected_include)
        self.assertEqual(eap.exclude, expected_exclude)
        self.assertEqual(eap.test, expected_test)
        self.assertEqual(eap.suite, expected_suite)
        self.assertEqual(eap.loglevel, expected_log_level)
        self.assertListEqual(
            sorted(['loglevel', 'include', 'test', 'exclude', 'suite', 'extension']),
            sorted(eap.robot_run_args.keys()))

    def test_get_log_html_output_location_default(self):
        """
        Test that get_log_html_output_location() returns the default location if one has not been specified
        """
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        expected_val = os.path.abspath(os.path.join(self.curr_dir, 'remote_log.html'))
        self.assertEqual(expected_val, actual_val)

    def test_get_log_html_output_location_outputdir_specified(self):
        """
        Test that get_log_html_output_location() returns the correct path when one is specified in the config
        """
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_log_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_log.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_log_html_output_location_log_specified_relative(self):
        """
        Test that get_log_html_output_location() returns the correct path when a relative one is specified in the config
        """
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
        """
        Test that get_log_html_output_location() returns the correct path when an absolute one is specified in the
        config
        """
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
        """
        Test that get_report_html_output_location() returns the default location if one has not been specified
        """
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        expected_val = os.path.join(self.curr_dir, 'remote_report.html')
        self.assertEqual(expected_val, actual_val)

    def test_get_report_html_output_location_outputdir_specified(self):
        """
        Test that get_report_html_output_location() returns the correct path when one is specified in the config
        """
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_report_html_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_report.html')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_report_html_output_location_log_specified_relative(self):
        """
        Test that get_report_html_output_location() returns the correct path when a relative one is specified in the
        config
        """
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
        """
        Test that get_report_html_output_location() returns the correct path when an absolute one is specified in the
        config
        """
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
        """
        Test that get_output_xml_output_location() returns the default location if one has not been specified
        """
        input_args = ['127.0.0.1', self.suite_dir]
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        expected_val = os.path.join(self.curr_dir, 'remote_output.xml')
        self.assertEqual(expected_val, actual_val)

    def test_get_output_xml_output_location_outputdir_specified(self):
        """
        Test that get_output_xml_output_location() returns the correct path when one is specified in the config
        """
        input_args = ['127.0.0.1',
                      self.suite_dir,
                      '--loglevel', 'DEBUG',
                      '--outputdir', '../../']
        eap = ExecutorArgumentParser(input_args)
        actual_val = eap.get_output_xml_output_location()
        expected_val = os.path.join(self.curr_dir, '..', '..', 'remote_output.xml')
        self.assertEqual(os.path.abspath(expected_val), os.path.abspath(actual_val))

    def test_get_output_xml_output_location_log_specified_relative(self):
        """
        Test that get_output_xml_output_location() returns the correct path when a relative one is specified in the
        config
        """
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
        """
        Test that get_output_xml_output_location() returns the correct path when an absolute one is specified in the
        config
        """
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
