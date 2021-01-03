import os
import logging
import six.moves.xmlrpc_client as xmlrpc_client
from robot.api import TestSuiteBuilder
from rfremoterunner.utils import normalize_xmlrpc_address, calculate_ts_parent_path
from rfremoterunner.robot_file_parser import RobotFileProcessor

logger = logging.getLogger(__file__)
DEFAULT_PORT = 1471


class RemoteFrameworkClient:

    def __init__(self, address, debug=False):
        """
        Constructor for RemoteFrameworkClient

        :param address: Hostname/IP of the server with optional :Port
        :type address: str
        :param debug: Run in debug mode. Enables extra logging and instructs the remote server not to cleanup the
        workspace after test execution
        :type debug: bool
        """
        self._address = normalize_xmlrpc_address(address, DEFAULT_PORT)
        self._client = xmlrpc_client.ServerProxy(self._address)
        self._debug = debug
        self._dependencies = {}
        self._suites = {}
        logger.setLevel(logging.DEBUG if debug else logging.INFO)

    def execute_run(self, suite_list, extensions, include_suites, robot_arg_dict):
        """
        Sources a series of test suites and then makes the RPC call to the
        agent to execute the robot run.

        :param suite_list: List of paths to test suites or directories containing test suites
        :type suite_list: list
        :param extensions: String that filters the accepted file extensions for the test suites
        :type extensions: str
        :param include_suites: List of strings that filter suites to include
        :type include_suites: list
        :param robot_arg_dict: Dictionary of arguments that will be passed to robot.run on the remote host
        :type robot_arg_dict: dict

        :return: Dictionary containing stdout/err, log html, output xml, report html, return code
        :rtype: dict
        """
        # Use robot to resolve all of the test suites
        suite_list = [os.path.normpath(p) for p in suite_list]
        logger.debug('Suite List: %s', str(suite_list))

        # Let robot do the heavy lifting in parsing the test suites
        builder = self._create_test_suite_builder(include_suites, extensions)
        suite = builder.build(*suite_list)

        # Now iterate the suite's family tree, pull out the suites with test cases and resolve their dependencies.
        # Package them up into a dictionary that can be serialized
        self._package_suite_hierarchy(suite)

        # Make the RPC
        logger.info('Connecting to: %s', self._address)
        response = self._client.execute_robot_run(self._suites, self._dependencies, robot_arg_dict, self._debug)

        return response

    @staticmethod
    def _create_test_suite_builder(include_suites, extensions):
        """
        Construct a robot.api.TestSuiteBuilder instance. There are argument name/type changes made at
        robotframework==3.2. This function attempts to initialize a TestSuiteBuilder instance assuming
        robotframework>=3.2, and falls back the the legacy arguments on exception.

        :param include_suites: Suites to include
        :type include_suites: list
        :param extensions: string of extensions using a ':' as a join character

        :return: TestSuiteBuilder instance
        :rtype: robot.api.TestSuiteBuilder
        """
        if extensions:
            split_ext = set(ext.lower().lstrip('.') for ext in extensions.split(':'))
        else:
            split_ext = ['robot']
        try:
            builder = TestSuiteBuilder(include_suites, included_extensions=split_ext)
        except TypeError:
            # Pre robotframework 3.2 API
            builder = TestSuiteBuilder(include_suites, extension=extensions) # pylint: disable=unexpected-keyword-arg

        return builder

    def _package_suite_hierarchy(self, suite):
        """
        Parses through a Test Suite and its child Suites and packages them up into a dictionary so they can be
        serialized

        :param suite: robot test suite
        :type suite: TestSuite
        """
        # Empty suites in the hierarchy are likely directories so we're only interested in ones that contain tests
        if suite.tests:
            # Use the actual filename here rather than suite.name so that we preserve the file extension
            suite_filename = os.path.basename(suite.source)
            self._suites[suite_filename] = self._process_test_suite(suite)

        # Recurse down and process child suites
        for sub_suite in suite.suites:
            self._package_suite_hierarchy(sub_suite)

    def _process_test_suite(self, suite):
        """
        Processes a TestSuite containing test cases and performs the following:
            - Parses the suite's dependencies (e.g. Library & Resource references) and adds them into the `dependencies`
            dict
            - Corrects the path references in the suite file to where the dependencies will be placed on the remote side
            - Returns a dict with metadata alongside the updated test suite file data

        :param suite: a TestSuite containing test cases
        :type suite: robot.running.model.TestSuite

        :return: Dictionary containing the suite file data and path from the root directory
        :rtype: dict
        """
        logger.debug('Processing Test Suite: `%s`', suite.name)
        # Traverse the suite's ancestry to work out the directory path so that it can be recreated on the remote side
        path = calculate_ts_parent_path(suite)

        suite_proc = RobotFileProcessor(suite)
        suite_proc.process_dependencies(self._dependencies)
        updated_file = suite_proc.get_updated_file_data()

        return {
            'path': path,
            'suite_data': updated_file
        }
