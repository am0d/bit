# File Hash Checker

import os
import sys
import subprocess

from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash, error_lookup

class HashDB(object):

    def __init__(self, name):
        self.name = name
        self.__location = '.buildit/{0}'.format(self.name)
        self.__file = None
        self.__dict = []
        self.__compile_list = []
        self.__run()

    def __run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'win32':
                subprocess.call('attrib +h .buildit')
        except:
            pass
        if not os.path.exists(self.__location):
            warning('Generating HashDB file.')
            try:
                self.file = open(self.__location, 'w')
                self.file.close()
            except IOError:
                error('Error: File IO Error')
        self.file = open(self.__location, 'r')
        for line in self.file:
            line = line.replace('\n', '')
            line = line.split(':')
            self.__dict.append(line)
        self.__dict = dict(tuple(self.__dict))

    def generate_hashfile(self, file_list):
        self.__file = open(self.__location, 'w')
        if sys.platform == 'win32':
            file_list = fix_strings(file_list)
        for file_name in file_list:
            self.__file.write('{0}:{1}\n'
        self.__file.close()

    @property
    def dictionary(self):
        return self.__dict

    def file_hash(self, file_name):
        return self.__dict.get(file_name, '')

    @property
    def compile_list(self):
        return self.__compile_list
