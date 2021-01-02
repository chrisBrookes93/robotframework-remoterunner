import argparse
import logging

from rfremoterunner.rf_server import RobotFrameworkServer

logger = logging.getLogger(__name__)


def run_agent_deprecated():
    """
    Pass through for the deprecated command line script. Displays a deprecation warning and calls through to the new
    entrypoint.
    """
    logger.warning('DeprecationWarning: "rfslave" command line has been deprecated and will be removed very soon inline'
                   ' with the movement to drop such terms. Please use "rfagent" instead')
    run_agent()


def run_agent():
    """
    Run the Robot Framework Agent
    """
    args = parse_args()
    rfc = RobotFrameworkServer(args.address, args.port, args.debug)
    rfc.serve()


def parse_args():
    """
    Parse the input arguments

    :return: Parsed input arguments
    :rtype: namespace
    """
    parser = argparse.ArgumentParser(description='Script to launch the robotframework Remote Runner Agent. This opens '
                                                 'an RPC port and waits for a request to execute a robot framework test'
                                                 ' execution')
    parser.add_argument('-a', '--address', help='Address to bind to. Default is 0.0.0.0', default='0.0.0.0')
    parser.add_argument('-p', '--port', help='Port to listen on. Default is 1471', default=1471, type=int)
    parser.add_argument('-d', '--debug', help='Enables debug logging and will not delete the temporary directory after '
                                              'a robot run',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    run_agent()
