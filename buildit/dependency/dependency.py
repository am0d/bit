# Base Dependency Class

import os
import sys

from buildit.utils import which, lookup_error, fix_strings
from buildit.cprint import command, warning, error

class Dependency(object):

    def __init__(self, name, directories=[]):
        self.name = name
        self._directories = directories
        self.__location = '.buildit/{0}.deps'.format(self.name)
        self.header = 'generic'
        self._magic_word = 'generic'
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

    def reset(self):
        ''' Resets the dependency list - only use this before generating
            the dependencies all over again
        '''
        self.__dependencies = {}

    def generate_dependencies(self):
        pass

    def parse_file(self, file_name):
        ''' Finds all the files that file_name depends on
            and adds it as a dependent of those files
        '''
        dependencies = []
        file = open(file_name, 'r')
        for line in file:
            if line.find(self._magic_word) > -1:
                name = self.parse_line(line, file_name)
                if not name == '':
                    dependencies.append(name)
        for name in dependencies:
            if not name in self.__dependencies:
                self.__dependencies[name] = []
            if not file_name in self.__dependencies[name]:
                self.__dependencies[name].append(file_name)

    # Leave implementation up to each language
    def parse_line(self, string, current_file):
        ''' Returns a formatted string for dependency searching '''
        line = string.partition(self._magic_word)
        line = line[2].strip()
        line = line.replace('<', '')
        line = line.replace('>', '')
        line = line.replace('"', '')
        line = line.replace("'", '')

        current_dir = os.path.split(current_file)[0]
        path = '{0}/{1}'.format(current_dir, line)
        path = os.path.normpath(path)
        if os.path.exists(path):
            return fix_strings([path])[0]
        for dir in self._directories:
            path = '{0}/{1}'.format(dir, line)
            if os.path.exists(path):
                return fix_strings([os.path.normpath(path)])[0]
        return ''

    def get_files_dependent_on(self, file_name):
        return self.__dependencies.get(file_name, [])

    def write_to_disk(self):
        try:
            self.file = open(self.__location, 'w')
            for file in self.__dependencies:
                for dependent in self.__dependencies[file]:
                    self.file.write('{0}:{1}\n'.format(file, dependent))
        except IOError:
            error('Unable to save dependencies to disk')
        finally:
            self.file.close()
