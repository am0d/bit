# File Hash Checker

import os
import sys

from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash, system_type

class HashDB(object):

    def __init__(self, hash_name):
        self.name = hash_name
        self.__location = '.buildit/{0}'.format(self.name)
        self.__file = None
        self.__dict = []
        self.__run()
        assert(isinstance(self.__dict, dict))

    def __run(self):
        try:
            os.makedirs('.buildit')
            if system_type == 'windows':
                subprocess.call('attrib +h .buildit')
        except:
            pass
        if not os.path.exists(self.__location):
            warning('HashDB file not found. Running first time generation')
            self.file = open(self.__location, 'w')
            self.file.close()
        self.file = open(self.__location, 'r')
        for line in self.file:
            line = line.replace('\n', '')
            line = line.split(':')
            self.__dict.append(line)
        self.__dict = dict(tuple(self.__dict))

    def generate_hashfile(file_list):
        self.__file.open(self.__location, 'w')
        if sys.platform == 'win32':
            file_list = fix_strings(file_list)
        for file_name in file_list:
            self._file.write('{0}:{1}\n'.format(file_name, \
                                                file_hash(file_name)))
        self.__file.close()

    @property        
    def dictionary(self):
        return self.__dict

    @property
    def file_hash(self, file_name):
        return self.__dict.get(file_name, '')

    
