# File Hash Checker

import os
import sys
import subprocess

from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash, lookup_error

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
            warning('Generating HashDB File.')
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

    def write(self):
        try: 
            self.__file = open(self.__location, 'w')
            for file_name in self.__dict:
                self.__file.write('{0}:{1}\n'.format(file_name, 
                    self.__dict[file_name]))
            self.__file.close()
        except IOError:
            error('Error: Could not generate HashDB')

    def has_changed(self, file_name):
        new_hash = file_hash(file_name)
        if file_name not in self.__dict:
            self.__dict[file_name] = new_hash
            return True
        elif not (new_hash == self.__dict[file_name]):
            self.__dict[file_name] = new_hash
            return True
        else:
            return False

    def remove_hash(self, file_name):
        ''' Removes a hash from the internal dictionary.
            Used by FileList to make sure that if a file didn't compile
            correctly, its hash will not be saved to disk, and therefore
            it will be compiled the next time we run. '''
        if file_name in self.__dict:
            del self.__dict[file_name]

    @property
    def dictionary(self):
        return self.__dict

    @property
    def compile_list(self):
        return self.__compile_list

