import io
import uuid
import re

PORT_INC_REGEX = '.*:[0-9]{1,5}$'


def read_file_from_disk(path):
    """
    Utility function to read and return a file from disk

    :param path: Path to the file to read
    :type path: str

    :return: Contents of the file
    :rtype: str
    """
    with open(path, 'rb') as fp:
        return fp.read()


def write_file_to_disk(path, file_contents):
    """
    Utility function to write a file to disk

    :param path: Path to write to
    :type path: str
    :param file_contents: Contents of the file
    :type file_contents: str
    """
    with open(path, 'wb') as fp:
        fp.write(file_contents)


def generate_temporary_directory_name():
    """
    Generate a random directory name to be used to store the test artifacts

    :return: unique directory name
    :rtype: str
    """
    return 'rf_workspace_{}'.format(uuid.uuid4())


def normalize_xmlrpc_address(address, default_port):
    """
    Normalises the server address by pre-pending with http:// if missing and appending :default_port if missing

    :param address: Address to normalise
    :type address: str
    :param default_port: Default port to append if missing
    :type default_port: int

    :return: Normalised address
    :rtype: str
    """
    if not re.match(re.compile(PORT_INC_REGEX), address):
        address = '{}:{}'.format(address, default_port)
    if not address.startswith(('http', 'https')):
        address = 'http://{}'.format(address)
    return address
