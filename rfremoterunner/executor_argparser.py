import argparse
import os

ROBOT_RUN_ARGS = ['loglevel', 'include', 'test', 'exclude', 'suite']


class ExecutorArgumentParser:

    def __init__(self, args):
        """
        Constructor for ExecutorArgumentParser
        
        :param args: Arguments to process (probably stdin)
        :type args: list
        """
        self._parser = self._init_parser()
        parsed_args = self._parser.parse_args(args)

        # Because of some limitations in argparse and not being able to specify multiple arguments of the same name,
        # we have to do some extra translation
        if parsed_args.suite:
            parsed_args.suite = parsed_args.suite.split(':')

        # Split the args based on whether they've for the executor, or whether they need to be passed to the robot run
        self.robot_run_args = {}
        for arg_name, arg_val in parsed_args.__dict__.items():
            if arg_name in ROBOT_RUN_ARGS:
                if arg_val is not None:
                    self.robot_run_args[arg_name] = arg_val
            setattr(self, arg_name, arg_val)


    @staticmethod
    def _init_parser():
        """
        Initialise the ArgumentParser instance with the supported arguments

        :return: Argument parser instance
        :rtype: ArgumentParser
        """
        parser = argparse.ArgumentParser(description='Script to execute a remote robot run')
        parser.add_argument('host',
                            help='IP or Hostname of the server to execute the robot run on. You can optionally specify '
                                 'the port the server is listening on by adding ":<port>". If not specified the port '
                                 'will be defaulted to 1471')
        parser.add_argument('suites', nargs='+',
                            help='One or more paths to test suites or directories containing test suites')
        parser.add_argument('--debug',
                            help='Run in debug mode. This will enable debug logging and does not cleanup the workspace '
                                 'directory on the remote machine after test execution', action='store_true')

        # Although these arguments are ones that robot accepts, they won't be passed into the remote robot execution.
        # The output artifacts will be placed in the workspace directory on the remote host and when pulled back they
        # are saved to the local machine as per configured by the arguments below
        parser.add_argument('-d', '--outputdir',
                            help='Where to create the output files on this machine once they\'ve been retrieved. The '
                                 'default is the directory that this script is run from')
        parser.add_argument('-o', '--output',
                            help='Where to save the XML output file on this machine once its been retrieved. Given '
                                 'path, similarly as paths given to --log and --report is path. Other output files are '
                                 'created based on XML output files after the test execution and XML outputs can also '
                                 'be further processed with Rebot tool. Default: remote_output.xml')
        parser.add_argument('-l', '--log',
                            help='Where to save the HTML Log file on this machine once its been retrieved. Default: '
                                 'remote_output.html')
        parser.add_argument('-r', '--report',
                            help='Where to save the HTML Report file on this machine once its been retrieved. Default: '
                                 'remote_output.html')

        # Although these arguments are ones that robot accepts, they won't be passed into the remote robot execution.
        # Instead they are used on the local machine to filter test suites so that unnecessary files are not
        # transferred over to the remote side.
        parser.add_argument('-F', '--extension',
                            help='Parse only files with this extension when executing a directory. Has no effect when '
                                 'running individual files or when using resource files. If more than one extension is '
                                 'needed, separate them with a colon.\r Examples: `--extension robot`, `-F robot:txt`')
        parser.add_argument('-s', '--suite',
                            help='Select test suites to run by name. When this option is used with --test, --include or'
                                 ' --exclude, only test cases in matching suites and also matching other filtering '
                                 'criteria are selected. Name can be a simple pattern similarly as with --test and it '
                                 'can contain parent name separated with a dot. You can specify multiple filters by '
                                 'concatenating with a colon. For example `-s X.Y` selects suite `Y` '
                                 'only if its parent is `X`. -s X:Y:Z selects X, Y & Z')

        # Arguments passed into the robot run on the remote host:
        parser.add_argument('-t', '--test',
                            help='Select test cases to run by name or long name. Name is case insensitive and'
                                 ' it can also be a simple pattern where `*` matches anything and `?` matches any '
                                 'char. To specify multiple, concatenate with a colon. Example: -t Foo*:Bar*')
        parser.add_argument('-i', '--include',
                            help='Select test cases to run by tag. Similarly as name  with --test, tag is case and '
                                 'space insensitive and it is possible to use patterns with `*` and `?` as wildcards. '
                                 'Tags and patterns can also be combined together with `AND`, `OR`, and `NOT` '
                                 'operators. Examples: --include foo, --include bar*, --include fooANDbar*')
        parser.add_argument('-e', '--exclude',
                            help='Select test cases not to run by tag. These tests are not run even if included with '
                                 '--include. Tags are matched using the rules explained with --include.')

        parser.add_argument('-L', '--loglevel',
                            help=' Threshold level for logging. Available levels: TRACE, DEBUG, INFO (default), WARN, '
                                 'NONE (no logging). Use syntax `LOGLEVEL:DEFAULT` to define the default visible log '
                                 'level in log files. Examples: --loglevel DEBUG --loglevel DEBUG:INFO')
        return parser

    def get_log_html_output_location(self):
        """
        Determine the local output file location of the log.html based on the input arguments

        :return: Path to where the log.html file should be saved
        :rtype: str
        """
        return self._resolve_output_path(self.log, 'remote_log.html')

    def get_output_xml_output_location(self):
        """
        Determine the local output file location of the output.xml based on the input arguments

        :return: Path to where the output.xml file should be saved
        :rtype: str
        """
        return self._resolve_output_path(self.output, 'remote_output.xml')

    def get_report_html_output_location(self):
        """
        Determine the local output file location of the report.html based on the input arguments

        :return: Path to where the report.html file should be saved
        :rtype: str
        """
        return self._resolve_output_path(self.report, 'remote_report.html')

    def _resolve_output_path(self, argument_val, filename):
        """
        Determine a path to output a file artifact based on whether the user specified the specific path

        :param argument_val: Value of the specific argument e.g. from --output
        :type argument_val: str
        :param filename: Name of the file e.g. log.html
        :type filename: str

        :return: Absolute path of where to save the test artifact
        :rtype: str
        """
        parent_dir = self.outputdir or '.'

        if argument_val:
            if os.path.isabs(argument_val):
                output_path = argument_val
            else:
                output_path = os.path.abspath(os.path.join(parent_dir, argument_val))
        else:
            output_path = os.path.abspath(os.path.join(parent_dir, filename))
        return output_path
