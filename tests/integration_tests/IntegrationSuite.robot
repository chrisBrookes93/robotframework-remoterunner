*** Settings ***
Library           Process
Library           OperatingSystem

*** Test Cases ***
Basic
    [Setup]
    # Start the slave
    ${slave_handle}=    Start Process    python    -m    rfslave.runslave
    Process Should Be Running    ${slave_handle}    Failed to launch the slave
    # Now run the Executor
    ${executor_result}=    Run Process    python    -m    rfslave.execute    127.0.0.1    ${CURDIR}/resources/
    Log    ${executor_result.stdout}
    Log    ${executor_result.stderr}
    File Should Exist    ${CURDIR}/output.xml
    File Should Exist    ${CURDIR}/log.html
    File Should Exist    ${CURDIR}/report.html
    [Teardown]    Basic Teardown

*** Keywords ***
Basic Teardown
    Terminate All Processes
    Remove Files    ${CURDIR}/output.xml    ${CURDIR}/log.html    ${CURDIR}/report.html
