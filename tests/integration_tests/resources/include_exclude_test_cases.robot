*** Settings ***

*** Test Cases ***
TC1
    [Tags]    AAA
    Log    1

TC2
    [Tags]    AAA
    Log    2

TC3
    [Tags]    AAA    CCC
    Log    3

TC4
    [Tags]    BBB
    Log    4

TC5
    [Tags]    BBB
    Log    5

TC6
    [Tags]    BBB
    Log    6
