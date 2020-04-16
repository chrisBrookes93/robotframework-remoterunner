# -*- coding: utf-8 -*-
import unittest
import tempfile
import shutil
import os
import six
from io import open
from robot.running.model import TestSuite
from rfremoterunner.utils import normalize_xmlrpc_address, calculate_ts_parent_path, read_file_from_disk, \
    write_file_to_disk


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.workspace = tempfile.mkdtemp()
        self.test_file1 = os.path.join(self.workspace, 'test_file1.txt')
        self.test_file2 = os.path.join(self.workspace, 'test_file2.txt')
        self.test_file3 = os.path.join(self.workspace, 'test_file3.txt')
        self.test_file1_data = u'ݼݼݼݼݼݼ' * 100
        with open(self.test_file1, 'w', encoding='utf-8') as fp:
            fp.write(self.test_file1_data)

    def tearDown(self):
        shutil.rmtree(self.workspace)

    def file_contents_is_equal(self, file_path, expected_file_data):
        """
        Helper function to verify the contents of a file

        :param file_path: Path to the file to verify
        :type file_path: str | unicode
        :param expected_file_data: Expected file data
        :type expected_file_data: str | unicode
        """
        if not os.path.exists(file_path):
            raise Exception('File does not exist:' + file_path)

        with open(file_path, 'r', encoding='utf-8') as fp:
            file_data = fp.read()
        self.assertEqual(expected_file_data, file_data)

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

    def test_read_file_from_disk(self):
        actual_data = read_file_from_disk(self.test_file1)
        self.assertEqual(self.test_file1_data, actual_data)

    def test_write_file_to_disk(self):
        file_data = u'ß' * 100
        write_file_to_disk(self.test_file2, file_data)
        self.file_contents_is_equal(self.test_file2, file_data)

    @unittest.skipIf(six.PY3, "Specific test for single-byte characters which is not relevant in Py3")
    def test_write_file_to_disk_str(self):
        file_data = 'A' * 100
        write_file_to_disk(self.test_file3, file_data)
        self.file_contents_is_equal(self.test_file3, file_data)

    def test_calculate_ts_parent_path(self):
        great_grandfather_ts = TestSuite()
        great_grandfather_ts.name = 'great-grandfather'
        grandfather_ts = TestSuite()
        grandfather_ts.name = 'grandfather'
        grandfather_ts.parent = great_grandfather_ts
        father_ts = TestSuite()
        father_ts.name = 'father'
        father_ts.parent = grandfather_ts
        ts = TestSuite()
        ts.parent = father_ts

        actual_value = calculate_ts_parent_path(ts)
        self.assertEqual(os.path.join('great-grandfather', 'grandfather', 'father'), os.path.normpath(actual_value))

    def calculate_ts_parent_path_no_parent(self):
        expected_value = ''
        ts = TestSuite()
        actual_value = calculate_ts_parent_path(ts)
        self.assertEqual(expected_value, actual_value)
