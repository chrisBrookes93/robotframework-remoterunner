*** Settings ***
Resource          ./primary_dependencies/Res1.robot
Library           ./primary_dependencies/Lib1.py
Library           ./primary_dependencies/secondary_dependencies/tertiary_dependencies/Lib3.py

*** Test Cases ***
TS1.1
    Res1 Keyword1
    Lib1 Keyword1
    Lib3 Keyword1
