import os
import logging
from six import StringIO
import six.moves.xmlrpc_client as xmlrpc_client
from robot.writer import DataFileWriter
from robot.running import TestSuiteBuilder
from robot.parsing.model import ResourceFile, TestCaseFile
from robot.libraries import STDLIBS
from robot.utils.robotpath import find_file
from rfremoterunner.utils import normalize_xmlrpc_address, read_file_from_disk, calculate_ts_parent_path


logger = logging.getLogger('rfremoterunner.executor')

DEFAULT_PORT = 1471
ROBOT_FILE_EXT = ('robot', 'txt', 'html')


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

    def execute_run(self, suite_list, extensions, include_suites, robot_arg_dict):
        """
        Sources a series of test suites and then makes the RPC call to the
        slave to execute the robot run.

        :param suite_list: List of paths to test suites or directories containing test suites
        :type suite_list: list
        :param extensions: String that filters the accepted files extensions for test suites
        :type extensions: str
        :param include_suites: List of strings that filter suites to include
        :type include_suites: list
        :param robot_arg_dict: Dictionary of arguments that will be passed to robot.run() on the remote host
        :type robot_arg_dict: dict

        :return: Dictionary containing stdout/err, log.html, output.xml, report.html, return code
        :rtype: dict
        """
        # Use robot to resolve all of the test suites
        suite_list = [os.path.normpath(p) for p in suite_list]
        logger.debug('Suite List: ' + str(suite_list))
        builder = TestSuiteBuilder(include_suites, extension=extensions)
        suite = builder.build(*suite_list)

        # Now iterate the suite's family tree, pull out the suites with test cases and resolve their dependencies.
        # Package them up into a dictionary that can be serialized
        self._package_suite_hierarchy(suite)

        # Make the RPC
        logger.info('Connecting to: ' + self._address)
        response = self._client.execute_robot_run(self._suites, self._dependencies, robot_arg_dict, self._debug)

        return response

    def _package_suite_hierarchy(self, suite):
        """
        Parses through a Test Suite and its child Suites and packages them up into a dictionary to can be serialized

        :param suite: root test suite
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
            - Corrects the path references to where the dependencies will be placed on the remote side
            - Returns a dict with metadata alongside the updated test suite file data

        :param suite: a TestSuite containing test cases
        :type suite: robot.running.model.TestSuite

        :return: Dictionary containing the suite file data and path from the root directory
        :rtype: dict
        """
        logger.debug('Processing Test Suite: `{}`'.format(suite.name))
        # Traverse the suite's ancestry to work out the directory path so that it can be recreated on the remote side
        path = calculate_ts_parent_path(suite)

        # At this point `suite` is a robot.running.model.TestSuite which doesn't appear to support writing the source
        # back to disk in robot syntax. To get around this, read it from disk again into a TestCaseFile which can be
        # modified and then converted into test suite file data
        tcf = TestCaseFile(source=suite.source).populate()

        # Iterate through the imports of suite. `_process_dependency()` will update the path to the reference which we
        # then copy to the TestCaseFile. From this we will produce the modified test suite file data
        for suite_imp, tcf_imp in zip(suite.resource.imports, tcf.imports):
            logger.debug('Processing dependency: `{}` for Test Suite: {}'.format(suite_imp.name, suite.name))
            self._process_dependency(suite_imp)
            tcf_imp.name = suite_imp.name

        # Now that we've updated the references, get the file contents
        string_io = StringIO()
        DataFileWriter(output=string_io).write(tcf)

        return {
            'path': path,
            'suite_data': string_io.getvalue()
        }

    def _process_dependency(self, dependency):
        """
        Processes a test suite dependency (could be a Resource or Library). This is read off the disk and added to the
        dependencies dict. This will then get transferred over to the remote side with the test suite. A dependency's
        location will be different on the remote host. This function also updates the reference to the dependency so
        that it resolves correctly on the remote side

        :param dependency: dependency to process
        :type dependency: robot.model.imports.Import
        """
        if dependency.name not in STDLIBS:
            # Locate the dependency file
            dep_filepath = find_file(dependency.name, dependency.directory, dependency.type)
            dep_filename = os.path.basename(dep_filepath)
            logger.debug('Resolved dependency to: `{}`'.format(dependency.name))

            # Change the path to the reference so that it will resolve on the remote side. The directory containing all of
            # the dependencies will be added to the PYTHONPATH, so just the filename is sufficient
            dependency.name = dep_filename

            if dep_filename not in self._dependencies:
                if dependency.type == 'Resource':
                    # Import the Resource in order to parse its dependencies
                    res = ResourceFile(dep_filepath).populate()

                    # A Resource may have a dependency on other Resource and Library file, also collect these
                    for imp in res.imports:
                        logger.debug('Processing dependency: `{}` for: `{}`'.format(imp.name, dependency.name))
                        self._process_dependency(imp)

                    # Get the resource file data with the new reference paths
                    string_io = StringIO()
                    res.save(output=string_io)
                    logger.debug('Patched Resource file: `{}`'.format(dependency.name))
                    self._dependencies[dep_filename] = string_io.getvalue()
                elif dependency.type == 'Library':
                    # We expect Robot StdLibs to already be present on the remote machine so don't bother packaging
                    # these

                    logger.debug('Reading Python library from disk: `{}`'.format(dep_filepath))
                    self._dependencies[dep_filename] = read_file_from_disk(dep_filepath)
            else:
                logger.debug('Dependency is already in the cache, skipping')

