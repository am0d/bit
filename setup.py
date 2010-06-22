#!/usr/bin/env python
# buildit install script

import os
import sys
import shutil

from distutils.core import setup

script_list = ['scripts/bit', 'scripts/bit.bat'] 
if not sys.platform == 'win32':
    script_list.remove('scripts/bit.bat')
if sys.platform == 'win32':
    if not os.path.exists('scripts/bit_script.py'):
        shutil.copyfile('scripts/bit', 'scripts/bit_script.py')
    script_list.remove('scripts/bit')
    script_list.append('scripts/bit_script.py')
setup(name='bit',
      version='0.3',
      license='BSD',
      description='A Minimal Build System',
      author='Tres Walsh',
      author_email='tres.walsh+bit@mnmlstc.com',
      url='http://mnmlstc.com',
      packages=['bit',
                'bit.project',
                'bit.compiler',
               ],
      scripts=script_list,
     )
