*** Settings ***
Documentation     Basic suite of tests for the execution of the slave and executor on the local machine.
Test Setup        Test Setup
Test Teardown     Test Teardown
Library           Process
Library           OperatingSystem
Library           Collections
Library           ../IntegrationTestLibs.py

*** Test Cases ***
Single Robot Test
    [Documentation]    Tests the remote execution of a basic named robot test
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/simple_suite.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html

Different Port
    [Documentation]    Tests that a specific port can be specified to run on
    ${port}=    Set Variable    1472
    # Start the slave on a specific port
    Start Slave    127.0.0.1    ${port}
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/simple_suite.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}
    ${ip}=    Set Variable    127.0.0.1:${port}
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html

Complex Case
    [Documentation]    Tests an in-depth example of a hierarchy of test suites. The robot suite hierarchy used in the unit tests for rf_client.py is re-used here
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../../unit_tests/rf_client_test_resources
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}    ${True}    ${test_workspace}/stdout.log    ${test_workspace}/stderr.log
    # To prevent the executor from hanging we need to send stdout/err to a file
    ${stdout}=    Get File    ${test_workspace}/stdout.log
    Log    ${stdout}    DEBUG
    ${stderr}=    Get File    ${test_workspace}/stderr.log
    Log    ${stderr}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html
    File Should Exist    ${test_workspace}/remote_output.xml
    # Verify the correct test cases executed
    ${expected_test_cases}=    Create List    S_TS2.1    S_TS3.1    S_TS4.1    T_TS5.1    T_TS6.1    TS1.1
    ${actual_test_cases}=    Get Test Executed Names    ${test_workspace}/remote_output.xml
    Lists Should Be Equal    ${expected_test_cases}    ${actual_test_cases}

Specific Extension
    [Documentation]    Test that the --extension parameter is passed to robot and behaves correctly. Note that file extensions other than .robot are deprecated. This test will cause robot to throw warnings
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/varying_file_extensions
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}    --extension=txt
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html
    ${expected_suites}=    Create List    Ts3    Ts4
    ${actual_suites}=    get_test_suite_names    ${test_workspace}/remote_output.xml
    Lists Should Be Equal    ${expected_suites}    ${actual_suites}

Suite Name Filtering
    [Documentation]    Tests the --suite variable correctly filters suites based on name
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/suite_name_filtering
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}    --suite=bbb*
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html
    ${expected_suites}=    Create List    Bbb Ts3
    ${actual_suites}=    Get Test Suite Names    ${test_workspace}/remote_output.xml
    Lists Should Be Equal    ${expected_suites}    ${actual_suites}

Specific Output Paths
    [Documentation]    Test that test artifacts are written to specific output paths when specified
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/simple_suite.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}    --log=custom_log.html    --report=custom_report.html    --output=custom_xml.xml
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/custom_xml.xml
    File Should Exist    ${test_workspace}/custom_log.html
    File Should Exist    ${test_workspace}/custom_report.html

Include Exclude Test Cases
    [Documentation]    Tests that the --include and --exclude arguments correctly filter test cases
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/include_exclude_test_cases.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}    --include=AAA    --exclude=CCC
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html
    ${expected_test_cases}=    Create List    TC1    TC2
    ${actual_test_cases}=    Get Test Executed Names    ${test_workspace}/remote_output.xml
    Lists Should Be Equal    ${expected_test_cases}    ${actual_test_cases}

Executor Correct Return Code
    [Documentation]    Tests that the executor returns the return code of the remote robot execution
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/suite_4_failing_tests.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}
    ${ip}=    Set Variable    127.0.0.1
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code. There should be 4 failing test cases so we expect 4
    Should Be Equal As Integers    ${executor_result.rc}    4    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html

Test uses Robot STDLIBs
    [Documentation]    Tests the correct remote execution of test suites that make use of Robot Standard Libraries
    # Start the slave
    Start Slave
    # Build arguments for the executor
    ${suite_list}=    Create List    ${CURDIR}/../resources/suite_with_stdlibs.robot
    ${arg_dict}=    Create Dictionary    --loglevel=TRACE    --outputdir=${test_workspace}
    ${ip}=    Set Variable    127.0.0.1:1471
    # Run the executor
    ${executor_result}=    Run Executor    ${ip}    ${suite_list}    ${arg_dict}
    Log    ${executor_result.stderr}    DEBUG
    Log    ${executor_result.stdout}    DEBUG
    # Check the return code
    Should Be Equal As Integers    ${executor_result.rc}    0    executerun failed with: ${executor_result.stderr}
    # Check the test artifacts were generated
    File Should Exist    ${test_workspace}/remote_output.xml
    File Should Exist    ${test_workspace}/remote_log.html
    File Should Exist    ${test_workspace}/remote_report.html

*** Keywords ***
Test Setup
    [Documentation]    Setup performed for each test. Creates a temporary workspace for the test to store artifacts
    ${test_workspace}=    Evaluate    tempfile.mkdtemp()    modules=tempfile
    Set Suite Variable    ${test_workspace}

Test Teardown
    [Documentation]    Teardown for all tests. Terminates any processes started by the test and deletes the temporary workspace
    Terminate All Processes
    Remove Directory    ${test_workspace}    recursive=${True}

Start Slave
    [Arguments]    ${ip}=127.0.0.1    ${port}=1471
    [Documentation]    Starts the slave executable
    # Start the slave
    ${command_line}=    Create List    rfslave    -a    ${ip}
    ...    -p    ${port}
    ${slave_handle}=    Start Process    @{command_line}    shell=${True}
    Sleep    2s
    Process Should Be Running    ${slave_handle}    Failed to launch the slave

Run Executor
    [Arguments]    ${ip}    ${suite_list}    ${arg_dict}    ${debug}=${False}    ${stdout_file}=${None}    ${stderr_file}=${None}
    [Documentation]    Runs the executor script
    ${command_line}=    Create Executor Command Line    ${ip}    ${suite_list}    ${arg_dict}    ${debug}
    ${executor_result}=    Run Process    @{command_line}    shell=${True}    stdout=${stdout_file}    stderr=${stderr_file}
    [Return]    ${executor_result}

Create Executor Command Line
    [Arguments]    ${ip}    ${suite_list}    ${arg_dict}    ${debug}=${False}
    [Documentation]    Creates a command line string for the executor
    ${cmd_line}=    Create List    rfremoterun    ${ip}
    : FOR    ${key}    IN    @{arg_dict.keys()}
    \    ${val}=    Get From Dictionary    ${arg_dict}    ${key}
    \    Append To List    ${cmd_line}    ${key}
    \    Append To List    ${cmd_line}    ${val}
    ${cmd_line}=    Combine Lists    ${cmd_line}    ${suite_list}
    Run Keyword If    ${debug}    Append To List    ${cmd_line}    --debug
    [Return]    ${cmd_line}
