# File Tracking Database

import os
import sys
import anydbm
import subprocess

from buildit.utils import flatten
from buildit.cprint import error

class Database(object):

    def __init__(self, name):
        self.name = name
        self.location = '.buildit/{0}'.format(self.name)
        self.run()
        try:
            self.hashdb = anydbm.open('{0}.hash'.format(self.location), 'c')
            self.depsdb = anydbm.open('{0}.deps'.format(self.location), 'c')
        except anydbm.error:
            error('Could not locate dependency databases!')

    def __del__(self):
        try:
            self.hashdb.close()
        except AttributeError:
            error('Could not close hash DB safely')
        try:
            self.depsdb.close()
        except AttributeError:
            error('Could not close dependency DB safely')

    def run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'win32':
                subprocess.call(['attrib', '+h', '.buildit'])
        except OSError:
            pass

    def get_hash(self, file_name): pass

    def update_hash(self, file_name): pass

    def get_deps(self, file_name): pass

    def update_deps(self, file_name): pass
