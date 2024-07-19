import unittest
from unittest.mock import patch, MagicMock
from pipresolver import get_versions, check_dependency, find_compatible_version

class TestPipResolver(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_versions(self, mock_run):
        mock_run.return_value = MagicMock(stdout="1.0.0\n2.0.0\n3.0.0")
        versions = get_versions("testpackage")
        self.assertEqual(versions, ['3.0.0', '2.0.0', '1.0.0'])

    @patch('subprocess.run')
    def test_check_dependency(self, mock_run):
        mock_run.return_value = MagicMock(stdout="testdep>=1.0.0,<2.0.0")
        result = check_dependency("testpackage", "1.0.0", "testdep", "1.5.0")
        self.assertEqual(result, "1.0.0")

    @patch('pipresolver.get_versions')
    @patch('pipresolver.check_dependency')
    def test_find_compatible_version(self, mock_check, mock_get_versions):
        mock_get_versions.return_value = ['3.0.0', '2.0.0', '1.0.0']
        mock_check.side_effect = [None, None, '1.0.0']
        result = find_compatible_version("testpackage", "testdep", "1.5.0")
        self.assertEqual(result, '1.0.0')

if __name__ == '__main__':
    unittest.main()
