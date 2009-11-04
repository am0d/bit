import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.depsdb import DepsDB

import monkey_patches

class TestDepsDB(unittest.TestCase):
    
    def setUp(self):
        self.include_dirs = []
        self.depsdb = DepsDB(self.include_dirs)
    
    def test_parse_includes(self):
        lines = {
                '' : '',
                '#include <stdio.h>' : '',
                '#include "../inc/test.h"' : '/home/test/buildit/inc/test.h',
                '#include "modules.h"' : '/home/test/buildit/src/modules.h',
                '#include "classes.hpp"' : '/home/test/buildit/src/classes.hpp',
                'int main() {' : '',
                '   return 0;' : '',
                '}' : ''
                }

        for line in lines:
            self.assertEqual(lines.get(line), self.depsdb.parse_line(line,
                                        '/home/test/buildit/src/main.cpp'))

if __name__ == '__main__':
    unittest.main()
