import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.system.system import System as System

class TestSystem(unittest.TestCase):
    
    def setUp(self):
        self.system = System("Test")

    def test_name(self):
        self.assertEqual('System', self.system.name)

if __name__ == '__main__':
    unittest.main()
