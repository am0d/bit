#Base Compiler Class

import os
import subprocess

from buildit.utils import which
from buildit.utils import flatten
from buildit.utils import fix_strings
from buildit.utils import name as uname
from buildit.cprint import command

class Compiler(object):
    
    def __init__(self):
        self._file_list = []
        self._compile_steps = []
        self._compile_flags = ''
        self._link_flags = ''
        self._executable = which('echo')
        self._type = '' # Added for much much later on
        self._object_directory = '.'
        self._build_directory = '.'

        self._compile_steps.append(self.setup_files)
        self._compile_steps.append(self.compile_files)
        self._compile_steps.append(self.link_files)

    def run(self, file_list, unity_build):
        self._file_list = file_list
        for function in self._compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0

    def setup_files(self):
        self._file_list = flatten(self._file_list)
        self._file_list = fix_strings(self._file_list)
        for file_name in self._file_list:
            for extension in self.extensions:
                if not file_name.endswith(extension):
                    self._file_list.remove(file_name)
        try:
            os.makedirs(self._object_directory)
        except:
            pass
        return 0

    # Leave the implementation up to each compiler
    def compile_files(self):
        pass

    def link_files(self):
        pass

    def _percentage(self, counter, list_length):
        ''' 
            Calculates the percentage of files completed, and returns it as a
            string 
        '''
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.')
        percentage = percentage.pop(0)
        return percentage

    def _info_string(self, percentage, file_name):
        ''' Prints out what file is being created '''
        command('[{0:>3}%] {1}: {2}'.format(
            percentage, self.name.upper(), file_name))

    def add_flags(self, flags):
        ''' Used mostly for compilers that have no link process '''
        self._compile_flags += format_options(flags)

    def add_compile_flags(self, flags):
        ''' Adds the flag to the compile steps '''
        self._compile_flags += format_options(flags)

    def add_link_flags(self, flags):
        ''' Adds the flag to the link step '''
        self._link_flags += format_options(flags)

    @property
    def executable(self):
        return which('echo')

    @executable.setter
    def executable(self, value):
        if isinstance(value, basestring):
            self._executable = which(value)

    @property
    def output_extension(self):
        return '.txt'

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
