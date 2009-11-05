# Base Dependency Class

import os
import sys

from buildit.utils import which, lookup_error
from buildit.cprint import command, warning

class Dependency(object):

    def __init__(self, name, directories=[]):
        self.name = name
        self._directories = directories
        self.__location = '.buildit/{0}.deps'.format(self.name)
        self.__dependencies = {}
        self.file = None
        self.language = None
        self.__run()

    def __run(self):
        try:
            os.makedirs('.buildit/')
            if sys.platform == 'win32':
                subprocess.call('attrib +h .buildit')
        except:
            pass
        if not os.path.exists(self.__location):
            warning('Generating dependency graph')
            try:
                self.file = open(self.__location, 'w')
                self.file.close()
            except IOError:
                error('Error: File IO Error')
        try:
            self.file = open(self.__location, 'r')
            self.language = self.file.readline()
            for line in self.file:
                line = line.replace('\n', '')
                line = line.split(':')
        except:
            error('Error: File IO Error')

