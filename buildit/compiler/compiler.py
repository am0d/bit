# Base Compiler Class

import os
import sys
import threading
import subprocess

from buildit.instance import buildit

from buildit.database import Database
from buildit.utils import which, flatten, hash
from buildit.cprint import command

class Compiler(object):

    def __init__(self, project_name, file_list):
        self.file_list = file_list
        self.completed_files =  [ ]
        self.compile_steps = [ ]
        self.compile_flags = [ ]
        self.file_extensions = ['txt']

        self.compiler_executable = which('echo')

        self.job_limit = 1 if buildit.options.job_limit < 1 else buildit.options.job_limit

        self.compile_steps.append(self.setup_files)
        self.compile_steps.append(self.compile_files)
        self.compile_steps.append(self.write_deps)

        self.output_directory = '.buildit/{0}/{1}'.format(self.project_name, self.name)
        self.output_extension = 'txt'
        self.internal_hash_tracker = { }

    def __str__(self):
        return 'Compiler'

    @property
    def run(self): 
        self.database = Database(self.project_name, self.name)
        for function in self.compile_steps:
            return_value = function()
            if not return_value:
                return return_value
        return 0

    def setup_files(self):
        self.file_list = list(set(flatten(self.file_list)))
        compile_list = [ ]
        proper_list = [ ]
        for extension in self.file_extensions:
            if file_name.endswith('.{0}'.format(extension)):
                proper_list.append(file_name)
        self.file_list = proper_list
        for file_name in self.file_list:
            file_hash = hash(file_name)
            out_file = '{0}/{1}.{2}'.format(self.output_directory, file_name, self.output_extension)
            if os.path.exists(out_file) and file_hash == self.database.get_hash(file_name):
                self.completed_files.append(file_name)
                continue
            self.internal_hash_tracker[file_name] = hash
            compile_list.append(file_name)
        self.file_list = list(set(compile_list)).sort()
        self.file_count = len(self.file_list)
        return 0

    # Most likely you'll override this EVERY TIME.
    def compile_files(self):
        return 0

    def write_deps(self):
        for key, value in self.internal_hash_tracker.iteritems():
            self.database.update_hash(key, value)

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

    @property
    def type(self):
        return self.project_type

    @type.setter
    def type(self, value):
        self.project_type = value
