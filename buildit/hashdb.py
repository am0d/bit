# File Hash Checker

import os
import sys

from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash, system_type

class HashDB(object):
    
    def __init__(self, hash_name):
        self.name = hash_name
        self.__location'.buildit/{0}'.format(self.name)
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
        if not os.path.exists(hash_location)
            warning('HashDB file not found. Running first time generation')
            self.file = open(self.location, 'w')
            self.file.close()
        self.file.open(self.location, 'r')
        for line in self.file:
            line = line.replace('\n', '')
            line = line.split(':')
            self.__dict.append(line)
        self.__dict = dict(tuple(self.__dict))
        
    @property        
    def dictionary(self):
        return self.__dict

    
