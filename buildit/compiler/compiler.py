# Base Compiler Class

import os
import sys
import threading
import subprocess

import buildit.buildit as buildit

from buildit.database import Database
from buildit.dependency import Dependency
from buildit.filehash import file_hash
from buildit.utils import which, flatten
from buildit.cprint import command

class Compiler(object):

    def __init__(self, project_name, file_list):
        self.file_list = file_list
        self.object_files = [ ]
        self.compile_steps = [ ]
        self.compile_flags = [ ]
        
        self.compiler_executable = which('echo')

        self.job_limit = 1 if buildit.options.job_limit < 1 \
                           else buildit.options.job_limit

        self.compile_steps.append(self.setup_files)
        self.compile_steps.append(self.compile_files)
        self.compile_steps.append(self.write_deps)

        self.object_directory = 'object/{0}/{1}'.format(self.project_name, 
                                                        self.name)
        self.dependency = Dependency()
        self.output_extension = 'txt'

    def __str__(self):
        return 'Compiler'

    @property
    def run(self):
        #TODO: Change database file/folder structure
        self.database = Database(self.project_name, self.name)
        for function in self.compile_steps:
            return_value = function()
            if not return_value:
                return return_value
        return self.object_files

    def setup_files(self):
        self.file_list = list(set(flatten(self.file_list)))
        compile_list = [ ]
        for file_name in self.file_list:
            for dep_ext in self.dependency.extensions:
                hash = file_hash.hash(file_name)
                out_file = '{0}/{1}.{2}'.format(self.object_directory, 
                                                file_name,
                                                self.output_extension)
                if os.path.exists(out_file) and \
                    hash == self.database.get_hash(file_name):
                        self.object_files.append(file_name)
                elif file_name.endswith(dep_ext) and \
                    not hash == self.database.get_hash(file_name):
                        pass
                        #TODO Write Dependency Parsing
                else:
                    compile_list.append(file_name)
        self.file_list = list(set(compile_list)).sort()
        self.file_count = len(self.file_list)
        return 0

    def compile_files(self):
        return 0

    def write_deps(self):
        return 0

    def percentage(self, counter, list_length):
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.').pop(0)
        return percentage

    def format_command(self, percentage, file_name):
        command('[{0:>3}%] {1}: {2}'.format(percentage, 
            str(self).upper(), file_name))

    def add_compiler_flags(self, *flags):
        flags = flatten(flags)
        for flag in flags:
            self.compile_flags.append(flag)

    @property
    def executable(self):
        return self.compiler_executable

    @executable.setter
    def executable(self, value):
        self.compiler_executable = which(value)

    @property
    def name(self):
        return self.__str__()
