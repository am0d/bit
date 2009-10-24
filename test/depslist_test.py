import os, sys
import unittest

# hack to make installing the modules unneccessary
# when running the tests
sys.path.insert(1, os.path.dirname(os.getcwd()))

from buildit.dependencies.depslist import Depslist as Depslist

import monkey_patches

class TestDepslist(unittest.TestCase):
    
    def setUp(self):
        self.include_dirs = []
        self.depslist = Depslist(self.include_dirs)
    
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

        self.depslist.current_file = '/home/test/buildit/src/main.cpp'

        for line in lines:
            self.assertEqual(lines.get(line), self.depslist.parse_line(line))

if __name__ == '__main__':
    unittest.main()
