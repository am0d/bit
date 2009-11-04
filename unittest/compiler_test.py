import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.compiler.compiler import Compiler as Compiler

class TestCompiler(unittest.TestCase):
    
    def setUp(self):
        self.compiler = Compiler()
    
    def test_name(self):
        self.assertEqual('Compiler', self.compiler.name)

if __name__ == '__main__':
    unittest.main()
