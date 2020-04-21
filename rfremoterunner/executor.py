import sys
import os
import logging
from rfremoterunner.utils import write_file_to_disk
from rfremoterunner.executor_argparser import ExecutorArgumentParser
from rfremoterunner.rf_client import RemoteFrameworkClient

logger = logging.getLogger('robotframework-remoterunner.executor')
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(message)s'))
out_hdlr.setLevel(logging.DEBUG)
logger.addHandler(out_hdlr)
logger.setLevel(logging.INFO)


def run_executor():
    """
    Initialise and run the executor
    """
    # Parse the input arguments
    arg_parser = ExecutorArgumentParser(sys.argv[1:])

    level = logging.DEBUG if arg_parser.debug else logging.INFO
    logger.setLevel(level)

    # Initialise and execute the remote robot run
    rfs = RemoteFrameworkClient(arg_parser.host, arg_parser.debug)
    result = rfs.execute_run(arg_parser.suites, arg_parser.extension, arg_parser.suite, arg_parser.robot_run_args)

    # Print the robot stdout/stderr
    logger.info('\nRobot execution response:')
    logger.info(result.get('std_out_err'))

    output_dir = arg_parser.outputdir or '.'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the log html, report html, output xml
    if result.get('output_xml'):
        output_xml_path = arg_parser.get_output_xml_output_location()
        write_file_to_disk(output_xml_path, result['output_xml'].data.decode('utf-8'))
        logger.info('Local Output:  ' + output_xml_path)

    if result.get('log_html'):
        log_html_path = arg_parser.get_log_html_output_location()
        write_file_to_disk(log_html_path, result['log_html'].data.decode('utf-8'))
        logger.info('Local Log:     ' + log_html_path)

    if result.get('report_html'):
        report_html_path = arg_parser.get_report_html_output_location()
        write_file_to_disk(report_html_path, result['report_html'].data.decode('utf-8'))
        logger.info('Local Report:  ' + report_html_path)

    sys.exit(result.get('ret_code', 1))


if __name__ == '__main__':
    run_executor()
