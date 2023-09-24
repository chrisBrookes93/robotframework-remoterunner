*** Settings ***
#Library   SCPLibrary
#Library    SerialLibrary    loop://    encoding=ascii
Library    C:/DEV/robotframework-remoterunner/tests/unit_tests/rf_client_test_resources/ConstructorTestLibrary.py    1    keyword_arg=2

*** Test Cases ***
#Grab Files From My Server
#    Run Keyword And Expect Error	*    Open Connection   192.168.1.42    username=tyler  password=teapot

Check Correct Passing Of Arguments Into Library
    ${pos_arg}=    get pos arg
    ${keyword_arg}=    get keyword arg
    should be equal  1    ${pos_arg}
    should be equal  2    ${keyword_arg}
