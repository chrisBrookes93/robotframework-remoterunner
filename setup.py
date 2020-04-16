import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='robotframework-remoterunner',
    version='1.1.0rc1',
    author='Chris Brookes',
    author_email='chris-brookes93@outlook.com',
    description='A library that provides the ability to execute RobotFramework test suites on a remote host. This comes'
                ' in the form of a lightweight agent that runs on the remote host, and an executor script that '
                'initiates the remote robot run. This is intended to used alongside or instead of other CI Agents.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url="https://github.com/chrisBrookes93/robotframework-remoterunner/archive/1.1.0.tar.gz",
    url='https://github.com/chrisBrookes93/robotframework-remotrunner',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Framework :: Robot Framework'
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'robotframework',
        'six'
    ]
)
