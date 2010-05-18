# File Tracking Database

import os
import sys
import shelve
import subprocess

from bit.utils import flatten, hash
from bit.cprint import error

class Database(object):

    def __init__(self, project_name, compiler_name):
        self.project_name = project_name
        self.compiler_name = compiler_name
        self.location = '.bit/{0}/{1}'.format(self.project_name, self.compiler_name)
        self.run
        self.hashdb = shelve.open('{0}.hash'.format(self.location), 'c', writeback=True)

    def __del__(self):
        try:
            self.hashdb.close()
        except ValueError:
            error('Could not close hash DB safely.')

    @property
    def run(self):
        try:
            os.makedirs(self.location)
            if sys.platform == 'win32':
                subprocess.call(['attrib', '+h', '.bit'])
        except OSError:
            pass

    def get_hash(self, file_name):
        if self.hashdb.has_key(file_name):
            return self.hashdb[file_name]
        return ''

    def update_hash(self, file_name, file_hash):
        self.hashdb[file_name] = str(file_hash)
        self.hashdb.sync()
