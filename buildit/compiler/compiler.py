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
        self._file_list = ""
        self._compile_steps = []
        self._compile_flags = ''
        self._link_flags = ''
        self.hashdb = ''
        self.project_name = ''
        self.parent = ''
        self._executable = which('echo')
        self._language = 'generic'
        self._object_directory = '.'
        self._build_directory = '.'
        self._unity_directory = '.'

        self._compile_steps.append(self.setup_files)
        self._compile_steps.append(self.compile_files)
        self._compile_steps.append(self.link_files)

    def run(self, file_list, parent, project_name='PROJECT'):
        self._file_list = file_list
        self.parent = parent
        self.project_name = project_name
        database = '{0}_{1}_{2}'.format(self.parent, 
                self.name, self.project_name)
        for function in self._compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0

    def setup_files(self):
        ''' Puts the appropriate files into the compile list. '''
        self._file_list.set_extensions(self.extensions)
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

    def hash_check(self, file_list):
        pass

    def _percentage(self, counter, list_length):
        ''' Returns the percentage of the current position in the list'''
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
    def unity_directory(self):
        return self._unity_directory

    @unity_directory.setter
    def unity_directory(self, value):
        self._unity_directory = value

    @property
    def extensions(self):
        return ['.txt']

    @property
    def name(self):
        return uname(self)
