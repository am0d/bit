# File Hash Checker

import os
import sys
import subprocess

from buildit.depsdb import DepsDB
from buildit.cprint import error, warning
from buildit.utils import fix_strings, file_hash

class HashDB(object):

    def __init__(self, hash_name):
        self.name = hash_name
        self.depsdb = DepsDB(self.name)
        self.__location = '.buildit/{0}'.format(self.name)
        self.__file = None
        self.__dict = []
        self.__compile_list = []
        self.__run()
        assert(isinstance(self.__dict, dict))

    def __run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'windows':
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

    def generate_hashfile(self):
        self.__file=open(self.__location, 'w')
        if sys.platform == 'win32':
            file_list = fix_strings(file_list)
        for file, hash in self.__dict.iteritems():
            self.__file.write('{0}:{1}\n'.format(file, hash))
        self.__file.close()

    def add(self, file_list):
        self.__file = open(self.__location, 'w')
        file_list = fix_strings(file_list)
        for file_name in file_list:
            file_name = file_name.replace('"', '')
            if file_name not in self.__dict:
                hash = file_hash(file_name)
                self.__dict[file_name] = hash
                if file_name not in self.__compile_list:
                    self.__compile_list.append(file_name)
                self.depsdb.parse_file(file_name)
                for dep in self.depsdb.get_dependencies(file_name):
                    if dep not in self.__compile_list:
                        self.__compile_list.append(dep)
            else:
                new_hash = file_hash(file_name)
                if not new_hash == self.__dict[file_name]:
                    if file_name not in self.__compile_list:
                        self.__compile_list.append(file_name)
                    self.__dict[file_name] = new_hash
                    self.depsdb.parse_file(file_name)
                    for dep in self.depsdb.get_dependencies(file_name):
                        if dep not in self.__compile_list:
                            self.__compile_list.append(dep)
        self.__file.close()
        self.depsdb.save_deps()

    @property 
    def dictionary(self):
        return self.__dict

    def file_hash(self, file_name):
        return self.__dict.get(file_name, '')

    @property
    def compile_list(self):
        return self.__compile_list

