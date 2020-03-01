import unittest
from rfremoterunner.utils import generate_temporary_directory_name, normalize_xmlrpc_address


class TestUtils(unittest.TestCase):

    def test_generate_temporary_directory_name_is_unique(self):
        dir_list = []
        for i in range(40):
            dir_list.append(generate_temporary_directory_name())
        self.assertEqual(len(dir_list), len(set(dir_list)))

    def test_normalize_xmlrpc_address_missing_protocol(self):
        input_val = 'google.com:1234'
        expected_val = 'http://google.com:1234'
        actual_val = normalize_xmlrpc_address(input_val, 1471)
        self.assertEqual(expected_val, actual_val)

    def test_normalize_xmlrpc_address_missing_port(self):
        input_val = 'http://10.20.30.40'
        expected_val = 'http://10.20.30.40:1471'
        actual_val = normalize_xmlrpc_address(input_val, 1471)
        self.assertEqual(expected_val, actual_val)



