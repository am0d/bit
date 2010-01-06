# Base Compiler Class

import os
import subprocess

from buildit.language.generic import Generic
from buildit.database import Database

from buildit.utils import which, flatten, fix_strings, file_hash
from buildit.utils import format_options
from buildit.utils import name as uname
from buildit.cprint import command as print_command

class Compiler(object):

    def __init__(self, project_name='PROJECT'):
        self._compile_steps = []
        self._type = 'binary'
        self._output_extension = '' # We normally won't have one.
        self._language = Generic()
        self._project_name = project_name
        self._compile_flags = ''
        self._link_flags = ''
        self._executable = which('echo')
        self._file_list = []
        self._link_list = []

        self._compile_steps.append(self.setup_files)
        self._compile_steps.append(self.compile_files)
        self._compile_steps.append(self.link_files)

    @property
    def run(self):
        self.database = Database(self._project_name)
        for function in self._compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0

    def setup_files(self):
        return 0

    # Leave the implementation up to each compiler
    def compile_files(self):
        return 0

    def link_files(self):
        return 0

    def parse_deps(self):
        return 0

    def _percentage(self, counter, list_length):
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.')
        percentage = percentage.pop(0)
        return percentage

    def command(self, percentage, file_name):
        print_command('[{0:>3}%] {1}: {2}'.format(percentage, 
            self.name.upper(), file_name))

    def add_flags(self, flags):
        self._compile_flags += format_options(flags)

    def add_compile_flags(self, flags):
        self._compile_flags += format_options(flags)

    def add_link_flags(self, flags):
        self._link_flags += format_options(flags)

    @property
    def output_extension(self):
        return self._output_extension

    @output_extension.setter
    def output_extension(self, value):
        self._output_extension = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def language(self):
        return self._language

    @property 
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        if isinstance(value, basestring):
            self._executable = which(value)

    @property
    def build_directory(self):
        return self._build_directory

    @build_directory.setter
    def build_directory(self, value):
        self._build_directory = value

    @property
    def object_directory(self):
        return self._object_directory

    @object_directory.setter
    def object_directory(self, value):
        self._object_directory = value

    @property
    def extensions(self):
        return ['.txt']

    @property
    def name(self):
        return uname(self)
