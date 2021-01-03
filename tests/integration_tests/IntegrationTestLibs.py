from robot.api import ExecutionResult


def get_test_suite_names(output_xml_path):
    """"
    Parses an output.xml file and returns the names of test suites that contain tests that were executed
    """
    ex_res = ExecutionResult(output_xml_path)
    return _recursively_list_test_suites(ex_res.suite)


def _recursively_list_test_suites(suite):
    """
    Recursively parses a test suite tree returns the names of test suites that contain tests that were executed
    """
    ret_val = []
    if suite.tests:
        ret_val.append(suite.name)

    for sub_suite in suite.suites:
        ret_val.extend(_recursively_list_test_suites(sub_suite))
    return ret_val


def get_test_executed_names(output_xml_path):
    """"
    Parses an output.xml file and returns the names of test cases that were executed
    """
    ex_res = ExecutionResult(output_xml_path)
    return _recursively_list_test_cases(ex_res.suite)


def _recursively_list_test_cases(suite):
    """
    Recursively parses a test suite tree and returns the names of test cases that were executed
    """
    ret_val = []
    for test in suite.tests:
        ret_val.append(test.name)

    for sub_suite in suite.suites:
        ret_val.extend(_recursively_list_test_cases(sub_suite))
    return ret_val
