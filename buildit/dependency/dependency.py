# Base Dependency Class

import os
import sys

from buildit.utils import which, lookup_error
from buildit.cprint import command, warning, error

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
            for line in self.file:
                line = line.replace('\n', '')
                line = line.split(':')
                if line[0] not in self.__dependencies:
                    self.__dependencies[line[0]] = []
                self.__dependencies[line[0]].append(line[1])
        except IOError:
            error('Error: File IO Error')
        finally:
            self.file.close()

    def generate_dependencies(self):
        pass

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

    def get_files_dependent_on(self, file_name):
        return self.__dependencies.get(file_name, [])
