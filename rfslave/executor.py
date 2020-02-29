"""
TODO -
Code refactor
README
Turn into a package
unit tests
Verify valid suites
send over suite Library & Resource dependencies
publish to PyPi

Feature List:
implement argparse
Async flag
fetch command
multiple machines
Python3 support - tox

Known issues:
Input args doesn't currently support multiple
Resources, Variable and Library files that a suite needs aren't currently shipped
"""
import sys
from rfslave.utils import write_file_to_disk
from rfslave.executor_argparser import ExecutorArgumentParser
from rfslave.rf_client import RemoteFrameworkClient


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
    write_file_to_disk(arg_parser.get_output_xml_output_location(), result['output_xml'])
    print 'Local Output:  ' + output_xml_path

    log_html_path = arg_parser.get_log_file_output_location()
    write_file_to_disk(log_html_path, result['log_html'])
    print 'Local Log:     ' + log_html_path

    report_html_path = arg_parser.get_report_html_output_location()
    write_file_to_disk(report_html_path, result['report_html'])
    print 'Local Report:  ' + report_html_path


if __name__ == '__main__':
    run_executor()
