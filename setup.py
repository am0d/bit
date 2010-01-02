#!/usr/bin/env python
# buildit install script

from distutils.core import setup

setup(name='buildit',
      version='0.2',
      license='BSD',
      description='A Minimal Build System',
      author='Tres Walsh',
      author_email='tres.walsh@mnmlstc.com',
      url='http://treswalsh.com',
      packages=['buildit',
                'buildit.system',
                'buildit.compiler',
                'buildit.language',
               ]
     )
