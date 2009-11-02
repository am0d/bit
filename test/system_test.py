import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.system.system import System as System

import monkey_patches

class TestSystem(unittest.TestCase):
    
    def setUp(self):
        self.system = System("Test")

    def test_name(self):
        self.assertEqual('System', self.system.name)

    def test_source_directory(self):
        self.system.source_directory = 'source'
        self.assertEqual('source', self.system.source_directory)

        self.system.source_directory = ''
        self.assertEqual('', self.system.source_directory)

    def test_build_directory(self):
        self.system.build_directory = 'build'
        self.assertEqual('build', self.system.build_directory)

        self.system.build_directory = ''
        self.assertEqual('', self.system.build_directory)

    def test_object_directory(self):
        self.system.object_directory = 'object'
        self.assertEqual('object', self.system.object_directory)

        self.system.object_directory = ''
        self.assertEqual('', self.system.object_directory)

        self.system.object_directory = ['object']
        self.assertEqual('object', self.system.object_directory)

    def test_unity_directory(self):
        self.system.unity_directory = 'unity'
        self.assertEqual('unity', self.system.unity_directory)

        self.system.unity_directory = ''
        self.assertEqual('', self.system.unity_directory)

if __name__ == '__main__':
    unittest.main()
