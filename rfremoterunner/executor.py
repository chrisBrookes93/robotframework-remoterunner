"""
TODO -
README
-h docs
unit tests
logging
Verify valid suites
send over suite Library & Resource dependencies
Python3 support - tox
Turn into a package
publish to PyPi

Feature List:
implement argparse
Async flag
fetch command
multiple machines


Known issues:
Input args doesn't currently support multiple
Resources, Variable and Library files that a suite needs aren't currently shipped
"""
import sys
from rfremoterunner.utils import write_file_to_disk
from rfremoterunner.executor_argparser import ExecutorArgumentParser
from rfremoterunner.rf_client import RemoteFrameworkClient


def run_executor():
    """
    Initialise and run the executor
    """
    # Parse the input arguments
    arg_parser = ExecutorArgumentParser(sys.argv[1:])

    # Initialize and execute the remote robot run
    rfs = RemoteFrameworkClient(arg_parser.host)
    result = rfs.execute_run(arg_parser.suites, arg_parser.robot_run_args)

    # Print the robot stdout/stderr
    print result.get('std_out_err')

    # Write the log.html, report.html, output.xml
    output_xml_path = arg_parser.get_output_xml_output_location()
    write_file_to_disk(arg_parser.get_output_xml_output_location(), unicode(result['output_xml']))
    print 'Local Output:  ' + output_xml_path

    log_html_path = arg_parser.get_log_file_output_location()
    write_file_to_disk(log_html_path, unicode(result['log_html']))
    print 'Local Log:     ' + log_html_path

    report_html_path = arg_parser.get_report_html_output_location()
    write_file_to_disk(report_html_path, unicode(result['report_html']))
    print 'Local Report:  ' + report_html_path


if __name__ == '__main__':
    run_executor()
