import argparse

from rfremoterunner.rf_server import RobotFrameworkServer


def run_slave():
    """
    Run the Robot Framework Slave
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
    parser = argparse.ArgumentParser(description='Script to launch the robotframework slave.')
    parser.add_argument('-a', '--address', help='Address to bind to. Default is localhost', default='127.0.0.1')
    parser.add_argument('-p', '--port', help='Port to listen on. Default is 1471', default=1471, type=int)
    parser.add_argument('-d', '--debug', help='If set the temporary directory will not be deleted after a robot run',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    run_slave()
