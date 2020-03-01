import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-remoterunner",
    version="1.0.0",
    author="Chris Brookes",
    description="A lightweight, standalone RobotFramework agent that can be used as an alternative to a Jenkins runslave. "
                "This runslave allows Robot Tests to be executed remotely. This package also includes the invoking script.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chrisBrookes93/robotframework-remotrunner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'robotframework',
        'six'
    ]
)










