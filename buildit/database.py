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
            self.depsdb = anydbm.open('{0}.deps'.format(self.location), 'c')
        except anydbm.error:
            error('Could not locate dependency databases')

    def __del__(self):
        try:
            self.hashdb.close()
        except AttributeError:
            error('Could not close hash DB safely')
        try:
            self.depsdb.close()
        except AttributeError:
            error('Could not close dependency DB safely')

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

    def update_hash(self, file_name):
        self.hashdb[file_name] = str(hash(file_name))
        self.hashdb.sync()

    def get_deps(self, file_name):
        return self.depsdb.get(file_name, '').split('|')

    def update_deps(self, file_name, dependencies):
        dependencies = '|'.join(flatten(dependencies))
        self.depsdb[file_name] = dependencies
        self.depsdb.sync()
