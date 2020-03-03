# Robot Framework Remote Runner

[![Build Status](https://gitlab.com/chrisBrookes93/robotframework-remoterunner/badges/develop/pipeline.svg)](https://gitlab.com/chrisBrookes93/robotframework-remoterunner)

This library provides a robotframework slave, and accompanying robot executor script that allows you to run 
Robot Framework Test Suites remotely. It's designed to be a lightweight agent and can be used as an alternative, 
or with a CI Agent (e.g. Jenkins Slave). The executor script parses Test Suites and packages them up before making an RPC 
call to the slave. The slave then writes all Test Suites and resources to a temporary directory and then executes a 
robot run, returning the test result artifacts back to the invoking host.

## Installation

Python Dependencies:
* robotframework
* six

To install the package run:
```text
pip install -r requirements.txt
```
This package will need to be installed on the slave host, and the host you wish to execute the remote run from.

## Usage:
This library contains two scripts:
* *runslave* - The agent that executes the robot run.
* *executerun* - The script that invokes the slave to execute the robot run.

### runslave

Once installed the slave can be launched by executing the ```rfremoterunner.runslave``` package:
```text
C:\python -m rfremoterunner.runslave -h
usage: __main__.py [-h] [-a ADDRESS] [-p PORT] [-d]

Script to launch the robotframework slave.

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address to bind to. Default is localhost
  -p PORT, --port PORT  Port to listen on. Default is 1471
  -d, --debug           If set the temporary directory will not be deleted after a robot run
```
Example usage:
```text
C:\python -m rfremoterunner.runslave -a 127.0.0.1 -p 1471
Listening on 127.0.0.1:1471
```

### executerun
Once installed a remote robot run can be executed by running the ````rfremoterunner.runslave```` package:
```text
C:\python -m rfremoterunner.executerun -h
usage: __main__.py [-h] [-d OUTPUTDIR] [-o OUTPUT] [-l LOG] [-r REPORT]
                   [-i INCLUDE] [-e EXCLUDE] [-t TEST] [-s SUITE]
                   [-L LOGLEVEL]
                   host suites [suites ...]

Script to execute a remote robot run

positional arguments:
  host                  IP or Hostname of the server to execute the robot run on. You can optionally specify the port the server is listening on by adding ":<port>". If not specified the
                        port will be defaulted to 1471
  suites                One or more paths to test suites or directories containing test suites

optional arguments:
  -h, --help            show this help message and exit
  -d OUTPUTDIR, --outputdir OUTPUTDIR
                        Where to create the output files on this machine once they've been retrieved. The default is the directory that this script is run from
  -o OUTPUT, --output OUTPUT
                        Where to save the XML output file on this machine once its been retrieved. Given path, similarly as paths given to --log and --report is path. Other output files
                        are created based on XML output files after the test execution and XML outputs can also be further processed with Rebot tool. Default: output.xml
  -l LOG, --log LOG     Where to save the HTML Log file on this machine once its been retrieved. Default: log.html
  -r REPORT, --report REPORT
                        Where to save the HTML Report file on this machine once its been retrieved. Default: report.html
  -i INCLUDE, --include INCLUDE
                        Select test cases to run by tag. Similarly as name with --test, tag is case and space insensitive and it is possible to use patterns with `*` and `?` as wildcards.
                        Tags and patterns can also be combined together with `AND`, `OR`, and `NOT` operators. Examples: --include foo --include bar* --include fooANDbar*
  -e EXCLUDE, --exclude EXCLUDE
                        Select test cases not to run by tag. These tests are not run even if included with --include. Tags are matched using the rules explained with --include.
  -t TEST, --test TEST  Select test cases to run by name or long name. Name is case and space insensitive and it can also be a simple pattern where `*` matches anything and `?` matches
                        any char.
  -s SUITE, --suite SUITE
                        Select test suites to run by name. When this option is used with --test, --include or --exclude, only test cases in matching suites and also matching other
                        filtering criteria are selected. Name can be a simple pattern similarly as with --test and it can contain parent name separated with a dot. For example `-s X.Y`
                        selects suite `Y` only if its parent is `X`.
  -L LOGLEVEL, --loglevel LOGLEVEL
                        Threshold level for logging. Available levels: TRACE, DEBUG, INFO (default), WARN, NONE (no logging). Use syntax `LOGLEVEL:DEFAULT` to define the default visible
                        log level in log files. Examples: --loglevel DEBUG --loglevel DEBUG:INFO
```
The executor script currently supports a subset of the arguments that ```robot.run``` supports.

Example usage:
```text
C:\python -m rfremoterunner.executerun 127.0.0.1 C:\DEV\robotframework-slave\tests\robot\ --loglevel DEBUG --outputdir ../
==============================================================================
T1                                                                            
==============================================================================
TC1                                                                   | PASS |
------------------------------------------------------------------------------
TC2                                                                   | FAIL |
'False' should be true.
------------------------------------------------------------------------------
T1                                                                    | FAIL |
2 critical tests, 1 passed, 1 failed
2 tests total, 1 passed, 1 failed
==============================================================================
Output:  C:\Users\user1\AppData\Local\Temp\rf_workspace_778f14bb-0dcb-46d1-a7ff-c8b9c5a9f2f0\output.xml
Log:     C:\Users\user1\AppData\Local\Temp\rf_workspace_778f14bb-0dcb-46d1-a7ff-c8b9c5a9f2f0\log.html
Report:  C:\Users\user1\AppData\Local\Temp\rf_workspace_778f14bb-0dcb-46d1-a7ff-c8b9c5a9f2f0\report.html

Local Output:  C:\DEV\robotframework-slave\tests\integration_tests\test_suites\remote_output.xml
Local Log:     C:\DEV\robotframework-slave\tests\integration_tests\test_suites\remote_log.html
Local Report:  C:\DEV\robotframework-slave\tests\integration_tests\test_suites\remote_report.html
```

## Current Limitations:
- Test Suites' Resource & Library files are not currently shipped down to the Robot Slave. 
- Because of limitations with ```argparse``` you are not able to specify some robot arguments multiple times like you can 
with ```robot.run``` (e.g. ```--include Tag1 --include Tag2```)

## Future Features:
- Ship over a Test Suite's Resource & Library dependencies. (Coming very soon!)
- Implement a ``--debug`` flag that will output verbose logs and will not delete the temporary directory on the slave 
machine after execution.
- Verify Test Suites are valid before invoking the slave runner.
- Extend Executor script to support all ```robot.run``` arguments.
- Add support for Robot Variable files.
- Implement custom argument parsing in the executor to allow for multiple arguments of the same name.
- Implement an asynchronous mode with the ability to poll the slave for a status on a particular robot execution.
- Add support to run on multiple hosts (concurrently).
