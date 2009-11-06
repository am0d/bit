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
        self.header = 'generic'
        self.__magic_word = 'generic'
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

    def generate_dependencies(self):
        self.file = open(self.__location, 'w')
        self.write('[{0}]'.format(self.header.upper()))
        self.close()

    def parse_file(self, file_name):
        ''' Returns a list of dependencies '''
        dependencies = []
        file = open(file_name, 'r')
        for line in file:
            if self.__magic_word in line:
                line = parse_line(line)
                dependencies.append(line)
        for name in dependencies:
            if not name in self.__dependencies:
                dependencies.remove(name)
        return dependencies

    # Leave implementation up to each language
    def parse_line(self, string):
        ''' Returns a formatted string for dependency searching '''
        return string

    
