import unittest
import os
import shutil
from io import open
from mock import patch
from rfremoterunner.rf_server import RobotFrameworkServer


class TestRobotFileParser(unittest.TestCase):

    pass


 # def test_process_test_suite(self):
    #
    #     def mock_process_dependency(dep):
    #         # Modify in some way so that we know we have the modified references is in the suite file data
    #         dep.name = os.path.basename(dep.name)
    #
    #     with patch('rfremoterunner.rf_client.RemoteFrameworkClient._process_dependency',
    #                side_effect=mock_process_dependency) as patched_process_dependency:
    #         result = self.test_obj._process_test_suite(self.ts1)
    #         suite_data = result.get('suite_data')
    #         self.assertEqual('Rf Client Test Resources', result.get('path'))
    #
    #         # Check that dependency are uppercase to check that they've been updated
    #         self.assertRegexpMatches(suite_data, 'Resource[\\s]+Res1\\.robot')
    #         self.assertRegexpMatches(suite_data, 'Library[\\s]+Lib1\\.py')
    #         self.assertRegexpMatches(suite_data, 'Library[\\s]+Lib3\\.py')
    #         patched_process_dependency.assert_any_call(self.ts1.resource.imports[0])
    #         patched_process_dependency.assert_any_call(self.ts1.resource.imports[1])
    #         patched_process_dependency.assert_any_call(self.ts1.resource.imports[2])
    #
    # def test_process_dependency_resource(self):
    #     imp = Import('Resource', './primary_dependencies/Res1.robot', source=self.ts1.source)
    #     self.test_obj._process_dependency(imp)
    #     # res1 (Res1.robot) has a dependency on Res2.robot & Lib3.py. Res2.robot has a dependency on Res3.robot & Lib3.py
    #     expected_dependencies = ['Res1.robot', 'Res2.robot', 'Res3.robot', 'Lib3.py']
    #     self.assertListEqual(sorted(expected_dependencies), sorted(self.test_obj._dependencies.keys()))
    #     # Check that the paths to dependencies have been updated
    #     self.assertRegexpMatches(self.test_obj._dependencies['Res3.robot'], 'Library[\\s]+Lib3\\.py')
    #     self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Library[\\s]+Lib3\\.py')
    #     self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Resource[\\s]+Res3\\.robot')
    #     self.assertRegexpMatches(self.test_obj._dependencies['Res1.robot'], 'Resource[\\s]+Res2\\.robot')
    #     self.assertRegexpMatches(self.test_obj._dependencies['Res2.robot'], 'Library[\\s]+Lib3\\.py')
    #
    # def test_process_dependency_library(self):
    #     imp = Import('Library', './primary_dependencies/Lib1.py', source=self.ts1.source)
    #     self.test_obj._process_dependency(imp)
    #     self.assertIn('Lib1.py', self.test_obj._dependencies)
    #     ts1_lib1_py_path = os.path.join(self.resource_dir, 'primary_dependencies', 'Lib1.py')
    #     self.assert_file_contents_is_equal(ts1_lib1_py_path, self.test_obj._dependencies['Lib1.py'])
    #
