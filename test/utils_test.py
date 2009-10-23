import os, sys
import unittest

# hack to make installing the modules uneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from  buildit.utils import *

class TestUtils(unittest.TestCase):
    
    def test_flatten_one_level(self):
        self.assertEqual(flatten([]),[])
        self.assertEqual(flatten(()),[])
        self.assertEqual(flatten(['hello']), ['hello'])
        self.assertEqual(flatten(('hello')), ['hello'])
        self.assertEqual(flatten(['hello', 'world']), ['hello', 'world'])
        self.assertEqual(flatten(('hello', 'world')), ['hello', 'world'])

    def test_flatten_two_levels(self):
        self.assertEqual(flatten([[]]), [])
        self.assertEqual(flatten((())), [])
        self.assertEqual(flatten([()]), [])
        self.assertEqual(flatten(([])), [])
        self.assertEqual(flatten([['one'], ['two']]), ['one', 'two'])
        self.assertEqual(flatten((('one'), ('two'))), ['one', 'two'])
        self.assertEqual(flatten([['one', 'two'],['three', 'four']]), ['one', 'two', 'three',
            'four'])
        self.assertEqual(flatten((('one', 'two'),('three', 'four'))), ['one', 'two', 'three',
            'four'])

if __name__ == "__main__":
   unittest.main() 
