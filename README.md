# Robot Framework Remote Runner

[![Build Status](https://github.com/chrisBrookes93/robotframework-remoterunner/workflows/CI/badge.svg?branch=main)](https://github.com/chrisBrookes93/robotframework-remoterunner/actions)
[![PyPI version](https://badge.fury.io/py/robotframework-remoterunner.svg)](https://badge.fury.io/py/robotframework-remoterunner)

This library provides a robotframework agent,
and accompanying robot executor script that allows you to execute Robot Framework Test Suites remotely.
It's designed to be a lightweight agent and can be used as an alternative,
or with a CI Agent (e.g. Jenkins Agent). The executor script parses Test Suites and packages them up with their dependencies before making an RPC call to the agent.
The agent then writes all Test Suites and resources to a temporary directory and executes a robot run,
returning the test result artifacts back to the invoking host.

This library is distinctly different, and not to be confused with [PythonRemoteServer](https://github.com/robotframework/PythonRemoteServer) 
which provides remote execution during a test run via the RemoteLib.

## Installation

Python Dependencies:
* robotframework >= 3.1.1
* six

To install the package and its runtime dependencies run:
```text
pip install robotframework-remoterunner
```
This package will need to be installed on the agent host, and the host you wish to execute the remote run from.

## Usage:
This library contains two scripts:
* *rfagent* - The agent that receives and executes the robot run.
* *rfremoterun* - The script that invokes the agent to execute the robot run.

### rfagent

Once installed, the agent can be launched by running the ```rfagent``` script:
```text
C:\>rfagent  -h
usage: rfagent [-h] [-a ADDRESS] [-p PORT] [-d]

Script to launch the robotframework agent. This opens an RPC port and waits
for a request to execute a robot framework test execution

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address to bind to. Default is 0.0.0.0
  -p PORT, --port PORT  Port to listen on. Default is 1471
  -d, --debug           Enables debug logging and will not delete the
                        temporary directory after a robot run
```
Example usage:
```text
C:\rfagent -a 192.168.56.102 -p 1471
Listening on 192.168.56.102:1471
```

### rfremoterun
Once installed, the a Test Suite can be executed remotely by running the ```rfremoterun``` script:
```text
C:\DEV>rfremoterun -h
usage: rfremoterun [-h] [--debug] [-d OUTPUTDIR] [-o OUTPUT] [-l LOG]
                   [-r REPORT] [-F EXTENSION] [-s SUITE] [-t TEST]
                   [-i INCLUDE] [-e EXCLUDE] [-L LOGLEVEL]
                   host suites [suites ...]

Script to initiate a remote robot framework test execution

positional arguments:
  host                  IP or Hostname of the server to execute the robot run
                        on. You can optionally specify the port the server is
                        listening on by adding ":<port>". If not specified the
                        port will be defaulted to 1471
  suites                One or more paths to test suites or directories
                        containing test suites

optional arguments:
  -h, --help            show this help message and exit
  --debug               Run in debug mode. This will enable debug logging and
                        does not cleanup the workspace directory on the remote
                        machine after test execution
  -d OUTPUTDIR, --outputdir OUTPUTDIR
                        Where to create the output files on this machine once
                        they've been retrieved. The default is the directory
                        that this script is run from
  -o OUTPUT, --output OUTPUT
                        Where to save the XML output file on this machine once
                        its been retrieved. Given path, similarly as paths
                        given to --log and --report is path. Other output
                        files are created based on XML output files after the
                        test execution and XML outputs can also be further
                        processed with Rebot tool. Default: remote_output.xml
  -l LOG, --log LOG     Where to save the HTML Log file on this machine once
                        its been retrieved. Default: remote_log.html
  -r REPORT, --report REPORT
                        Where to save the HTML Report file on this machine
                        once its been retrieved. Default: remote_report.html
  -F EXTENSION, --extension EXTENSION
                        Parse only files with this extension when executing a
                        directory. Has no effect when running individual files
                        or when using resource files. If more than one
                        extension is needed, separate them with a colon.
                        Examples: `--extension robot`, `-F robot:txt`
  -s SUITE, --suite SUITE
                        Select test suites to run by name. When this option is
                        used with --test, --include or --exclude, only test
                        cases in matching suites and also matching other
                        filtering criteria are selected. Name can be a simple
                        pattern similarly as with --test and it can contain
                        parent name separated with a dot. You can specify
                        multiple filters by concatenating with a colon. For
                        example `-s X.Y` selects suite `Y` only if its parent
                        is `X`. -s X:Y:Z selects X, Y & Z
  -t TEST, --test TEST  Select test cases to run by name or long name. Name is
                        case insensitive and it can also be a simple pattern
                        where `*` matches anything and `?` matches any char.
                        To specify multiple, concatenate with a colon.
                        Example: -t Foo*:Bar*
  -i INCLUDE, --include INCLUDE
                        Select test cases to run by tag. Similarly as name
                        with --test, tag is case and space insensitive and it
                        is possible to use patterns with `*` and `?` as
                        wildcards. Tags and patterns can also be combined
                        together with `AND`, `OR`, and `NOT` operators.
                        Examples: --include foo, --include bar*, --include
                        fooANDbar*
  -e EXCLUDE, --exclude EXCLUDE
                        Select test cases not to run by tag. These tests are
                        not run even if included with --include. Tags are
                        matched using the rules explained with --include.
  -L LOGLEVEL, --loglevel LOGLEVEL
                        Threshold level for logging. Available levels: TRACE,
                        DEBUG, INFO (default), WARN, NONE (no logging). Use
                        syntax `LOGLEVEL:DEFAULT` to define the default
                        visible log level in log files. Examples: --loglevel
                        DEBUG --loglevel DEBUG:INFO

```
The executor script currently supports a subset of the arguments that ```robot.run``` supports.

Example usage:
```text
C:\DEV> rfremoterun 192.168.56.102 C:\DEV\robotframework-remoterunner\tests\robot\ --loglevel DEBUG --outputdir ./
Connecting to: http://192.168.56.102:1471

Robot execution response:
==============================================================================
Root
==============================================================================
Root.TS1
==============================================================================
TS1.1                                                                 | PASS |
------------------------------------------------------------------------------
Root.TS1                                                              | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
==============================================================================
Root                                                                  | PASS |
1 critical test, 1 passed, 0 failed
1 test total, 1 passed, 0 failed
==============================================================================
Output:  c:\users\user1\appdata\local\temp\tmpy26cmp\output.xml
Log:     c:\users\user1\appdata\local\temp\tmpy26cmp\log.html
Report:  c:\users\user1\appdata\local\temp\tmpy26cmp\report.html

Local Output:  C:\DEV\remote_output.xml
Local Log:     C:\DEV\remote_log.html
Local Report:  C:\DEV\remote_report.html
```

## Issues/Limitations:
- HTTPS is not yet supported
- Any Python Keyword libraries' dependencies are not packaged up and sent to the remote host.
  Any external Python packages that the Keywords rely on will need to be installed on the remote host.
- It is strongly recommended to run the agent and the executor against the same version of robotframework.
There are subtle differences in the way robotframework parses arguments and you may experience unexpected behaviour.
- Although there is backward support for earlier versions of robotframework, this package assumes modern versions. 
You should take care that your underlying robotframework version supports the arguments that you require.

## Future Features:
- Add support for HTTPS
- Extend Executor script to support all ```robot.run``` arguments.
- Add support for Robot Variable files.
- Implement an asynchronous mode with the ability to poll the agent for a status on a particular robot execution.
- Add support to run on multiple hosts (concurrently).
