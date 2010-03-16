#!/usr/bin/env python
# buildit install script

import os

from distutils.core import setup
from glob import glob

script_list = glob('{0}/scripts/*'.format(os.getcwd()))
script_list = list(set([item.replace('~', '') for item in script_list]))
setup(name='buildit',
      version='0.2',
      license='BSD',
      description='A Minimal Build System',
      author='Tres Walsh',
      author_email='tres.walsh@mnmlstc.com',
      url='http://mnmlstc.com',
      packages=['buildit',
                'buildit.platform',
                'buildit.compiler',
                'buildit.parser'
               ],
      scripts=script_list,
     )
