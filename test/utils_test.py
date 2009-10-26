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

    def test_system_type(self):
        sys.platform = 'win32'
        self.assertEqual('windows', system_type())
        sys.platform = 'cygwin'
        self.assertEqual('windows', system_type())
        sys.platform = 'linux'
        self.assertEqual('linux', system_type())
        sys.platform = 'linux2'
        self.assertEqual('linux', system_type())
        sys.platform = 'darwin'
        self.assertEqual('apple', system_type())
        sys.platform = ''
        self.assertEqual('generic', system_type())
        sys.platform = 'unknown'
        self.assertEqual('generic', system_type())

    def test_format_options(self):
        options = ['all', 'error', 'typos', 'etc']
        self.assertEqual(' all error typos etc', format_options(options))
        self.assertEqual(' -Wall -Werror -Wtypos -Wetc', format_options(options, '-W'))

if __name__ == "__main__":
   unittest.main() 
