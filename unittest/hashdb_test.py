import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.hashdb import HashDB as HashDB

import monkey_patches

class TestHashDB(unittest.TestCase):
    
    def setUp(self):
        self.hashdb = HashDB('Test')

    def test_run(self):
        self.assertEqual('', self.hashdb.file_hash(''))
    
if __name__ == '__main__':
    unittest.main()
