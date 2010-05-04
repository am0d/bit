#!/usr/bin/env python
# buildit install script

import os
import sys
from distutils.core import setup
from glob import glob


script_list = ['scripts/snake', 'scripts/snake.bat'] 
if not sys.platform == 'win32':
    script_list.remove('scripts/snake.bat')
setup(name='buildit',
      version='0.3',
      license='BSD',
      description='A Minimal Build System',
      author='Tres Walsh',
      author_email='tres.walsh@mnmlstc.com',
      url='http://mnmlstc.com',
      packages=['buildit',
                'buildit.project',
                'buildit.compiler',
               ],
      scripts=script_list,
     )
