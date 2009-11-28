# File Database Class
import os
import sys
import anydbm
import os
import sys

from buildit.utils import file_hash, error

class Database(object):

    def __init__(self, project_name, language):
        self.__project_name = project_name
        self.__language = language
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
        try:
            self.__hashdb = anydbm.open('{0}.hash'.format(self.__location), 'c')
            self.__depsdb = anydbm.open('{0}.deps'.format(self.__location), 'c')
        except anydbm.error:
            print 'Error opening configuration files'

        self.__run()
        # We need to fill the hash_dictionary.

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
        #self.update_hash()
        pass

    def get_hash(self, file_name):
        # Ensure that the hash returned is a string.
        return str(self.hashdb[file_name])

    def update_hash(self, file_name):
        self.__hashdb[file_name] = file_hash(file_name)
        self.__hashdb.sync()

    def write_hashes(self, file_list):
        for file_name in file_list:
            self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    def write_deps(self, file_list):
        #for file_name in file_list:
        #    self.depsdb[file_name]
        self.__depsdb.sync()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, object):
            self.__language = value
