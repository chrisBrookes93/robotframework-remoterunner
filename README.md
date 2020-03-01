Robot Framework Remote Runner

Usage:


Current Limitations:
- Because of limitations with argparse you are not able to specify some robot arguments multiple times like you can with robot run (e.g. --include Tag1 --include Tag2)
- Test Suites' Resource & Library files are not currently shipped down to the Robot Slave

Future Features:
- Verify Test Suites are valid before invoking the slave runner
- Ship over a Suite's Resource & Library dependencies
- Add support for Robot Variable files
- Implement custom argument parsing in the executor to allow for multiple arguments of the same name
- Implement an asynchronous mode with the ability to poll the slave for a status on a robot execution
- Add support to run on multiple machines (concurrently)