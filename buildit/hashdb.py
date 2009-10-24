# File Hash Checker

import os
import sys

from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash

class HashDB(object):
    
    def __init__(self, hash_name):
        self.name = hash_name
        self.location'.buildit/{0}'.format(self.name)
        self.file = None
        self.dict = None
        self.run()

    def run(self):
        try:
            os.makedirs('.buildit')
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
            self.dict.append(line)
        self.dict = dict(list(self.dict))
        
    @property        
    def dictionary(self):
        return self.dict

    
