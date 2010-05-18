# Base Compiler Class

import os
import sys
import threading
import subprocess

from bit.instance import bit

from bit.database import Database
from bit.utils import which, flatten, hash
from bit.cprint import command

class Compiler(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.file_list = [ ]
        self.link_list = [ ]
        self.build_steps = [ ]

        self.compiler_flags = [ ]
        self.linker_flags = [ ]
        self.internal_hash_tracker = { }

        self.compiler_executable = which('echo')
        self.linker_executable = which('echo')
    
        self.build_steps.append(self.setup_files)
        self.build_steps.append(self.compile_files)
        self.build_steps.append(self.write_deps)
        self.build_steps.append(self.link_files)

        self.object_directory = '.bit/{0}/{1}'.format(self.project_name, self.name)
        self.build_directory = 'build/{0}'.format(self.project_name)
        self.output_extension = 'txt'
        
    def __str__(self):
        return 'Compiler'

    def __repr__(self):
        return 'Name: {0}\nOutput Directory: {1}\nExecutables: {2}|{3}\n'.format(self.name, 
                self.build_directory, self.compiler_executable, self.linker_executable)
    
    @property
    def run(self):
        for function in self.build_steps:
            return_value = function()
            if return_value:
                return return_value
        del self.database
        return 0

    def setup_files(self):
        self.database = Database(self.project_name, self.name)
        self.file_list = list(set(flatten(self.file_list)))
        proper_list = [ ]
        compile_list = [ ]
        for extension in self.extensions:
            for file_name in self.file_list:
                if file_name.endswith(extension):
                    proper_list.append(file_name)
        self.file_list = proper_list
        for file_name in self.file_list:
            file_hash = hash(file_name)
            out_file = '{0}/{1}.{2}'.format(self.object_directory, file_name, 
                                            self.output_extension)
            if os.path.exists(out_file) and file_hash == self.database.get_hash(file_name):
                self.link_list.append(file_name)
                continue
            compile_list.append(file_name)
            self.internal_hash_tracker[file_name] = file_hash
        self.file_list = list(set(compile_list))
        self.file_count = len(self.file_list)
        return 0

    def write_deps(self):
        for key, value in self.internal_hash_tracker.iteritems():
            self.database.update_hash(key, value)
        return 0
    
    # Should Override
    def compile_files(self):
        return 0

    # Should Override
    def link_files(self):
        return 0

    def percentage(self, counter, list_length):
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.').pop(0)
        return percentage

    def format_command(self, percentage, file_name):
        command('[{0:>3}%] {1}: {2}'.format(percentage, self.name.upper(), file_name))

    def add_compiler_flags(self, *flags):
        for flag in flatten(flags):
            self.compiler_flags.append(flag)

    def add_linker_flags(self, *flags):
        for flag in flatten(flags):
            self.linker_flags.append(flags)

    @property
    def compiler(self):
        return self.compiler_executable

    @compiler.setter
    def compiler(self, value):
        self.compiler_executable = which(value)

    @property
    def name(self):
        return self.__str__()
