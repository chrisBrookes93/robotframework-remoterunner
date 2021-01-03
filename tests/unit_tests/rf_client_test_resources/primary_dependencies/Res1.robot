*** Settings ***
Resource    ./secondary_dependencies/Res2.robot
Library    ./secondary_dependencies/tertiary_dependencies/Lib3.py

*** Keywords ***
Res1 Keyword1
    Log    K1
