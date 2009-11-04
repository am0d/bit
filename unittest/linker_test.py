import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.linker.linker import Linker as Linker

class TestLinker(unittest.TestCase):
    
    def setUp(self):
        self.linker = Linker()
    
    def test_name(self):
        self.assertEqual('Linker', self.linker.name)

if __name__ == '__main__':
    unittest.main()
