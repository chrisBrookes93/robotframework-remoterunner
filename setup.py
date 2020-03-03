import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='robotframework-remoterunner',
    version='1.0.1',
    author='Chris Brookes',
    description='This library provides a robotframework slave, and accompanying robot executor script that allows you '
                'to run Robot Framework Test Suites remotely. It\'s designed to be a lightweight agent and can be used '
                'as an alternative, or with a CI Agent (e.g. Jenkins Slave).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    download_url="https://github.com/chrisBrookes93/robotframework-remoterunner/archive/1.0.1.tar.gz",
    url='https://github.com/chrisBrookes93/robotframework-remotrunner',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
       'robotframework',
        'six'
    ]
)










