# File Database Class
import os
import sys
import anydbm
import subprocess

from buildit.utils import file_hash, error
from buildit.utils import flatten
from buildit.language.generic import Generic

# We use the pipe (|) character to separate the files, 
# because no operating system allows a | in the file name, 
# and if it does that's just dumb XD

class Database(object):

    def __init__(self, project_name):
        self.__project_name = project_name
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.__run()
        try:
            # File Hashes
            self.__hashdb = anydbm.open('{0}.hash'.format(self.__location), 'c')
            # Dependency Lists
            self.__depsdb = anydbm.open('{0}.deps'.format(self.__location), 'c')
            # Dependency File Hashes
            self.__dfhsdb = anydbm.open('{0}.dfhs'.format(self.__location), 'c')
        except anydbm.error:
            error('Could not open dependency databases')

    def __del__(self):
        try:
            self.__hashdb.close()
        except AttributeError:
            error('Could not close HashDB safely')
        try:
            self.__depsdb.close()
        except AttributeError:
            error('Could not close DepsDB safely')
        try:
            self.__dfhsdb.close()
        except AttributeError:
            error('Could not close DFHSDB safely')

    def __run(self):
        try:
            os.makedirs('.buildit')
            # Keep the folder hidden on windows.
            if sys.platform == 'win32':
                subprocess.call(['attrib', '+h', '.buildit'])
        except OSError:
            pass

    def get_hash(self, file_name):
        return str(self.__hashdb.get(file_name, ''))

    def update_hash(self, file_name):
        self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    def write_hashes(self, file_list):
        for file_name in file_list:
            self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    # Returns a list, so pay attention.
    def get_deps(self, file_name):
        return self.__depsdb.get(file_name, '').split('|')[1:]

    def add_deps(self, file_name, dependents):
        if file_name not in self.__depsdb:
            self.__depsdb[file_name] = ''
        dependents = flatten(dependents)
        dependency_string = '|'.join(dependents)
        self.__depsdb[file_name] = '{0}|{1}'.format(
            self.__depsdb[file_name], dependency_string)
        self.__depsdb.sync()

    def get_dfhs(self, file_name):
        return str(self.__dfhsdb.get(file_name, ''))

    def update_dfhs(self, file_name):
        self.__dfhsdb[file_name] = str(file_hash(file_name))
        self.__dfhsdb.sync()

    def write_dfhs(self, file_list):
        for file_name in flatten(file_list):
            self.__dfhsdb[file_name] = str(file_hash(file_name))
        self.__dfhsdb.sync()
