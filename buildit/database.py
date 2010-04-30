# File Tracking Database

import os
import sys
import anydbm
import subprocess

from buildit.utils import flatten, hash
from buildit.cprint import error

class Database(object):

    def __init__(self, project_name, compiler_name):
        self.project_name = project_name
        self.compiler_name = compiler_name
        self.location = '.buildit/{0}/{1}'.format(self.project_name, self.compiler_name)
        self.run
        try:
            self.hashdb = anydbm.open('{0}.hash'.format(self.location), 'c')
        except anydbm.error:
            error('Could not locate hash database')

    def __del__(self):
        try:
            self.hashdb.close()
        except AttributeError:
            error('Could not close hash DB safely.')

    @property
    def run(self):
        try:
            os.makedirs(self.location)
            if sys.platform == 'win32':
                subprocess.call(['attrib', '+h', '.buildit'])
        except OSError:
            pass

    def get_hash(self, file_name):
        return self.hashdb.get(file_name, '')

    def update_hash(self, file_name, file_hash):
        self.hashdb[file_name] = str(file_hash)
        self.hashdb.sync()
