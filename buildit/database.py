# File Database Class
import os
import sys
import anydbm
import subprocess

from buildit.utils import file_hash, error
from buildit.utils import flatten
from buildit.language.generic import Generic

class Database(object):

    def __init__(self, project_name):
        self.__project_name = project_name
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.__run()
        try:
            self.__hashdb = anydbm.open('{0}.hash'.format(self.__location), 'c')
            self.__depsdb = anydbm.open('{0}.deps'.format(self.__location), 'c')
        except anydbm.error:
            error('Could not open dependency databases')

    def __del__(self):
        try:
            self.__hashdb.close()
        except AttributeError:
            pass
        try:
            self.__depsdb.close()
        except AttributeError:
            pass

    def __run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'win32':
                subprocess.call('attrib +h .buildit')
        except OSError:
            pass

    def get_hash(self, file_name):
        # Ensure that the hash returned is a string.
        return str(self.__hashdb.get(file_name, ''))

    def update_hash(self, file_name):
        self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    def write_hashes(self, file_list):
        for file_name in file_list:
            self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    def get_deps(self, file_name):
        return self.__depsdb.get(file_name, '').split('|')[1:]

    def add_deps(self, file_name, dependents):
        if file_name not in self.__depsdb:
            self.__depsdb[file_name] = ''
        dependents = flatten(dependents)
        for dep in dependents:
            self.__depsdb[file_name] = '{0}|{1}'.format(
                self.__depsdb[file_name], dep)

    def write_deps(self, file_list):
        #for file_name in file_list:
        #    self.depsdb[file_name]
        self.__depsdb.sync()

    def find_deps(self, language, file_list):
        pass

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, object):
            self.__language = value
