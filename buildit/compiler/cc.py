# Unix Based C Compiler

import os
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.utils import which
from buildit.cprint import command

class CC(Compiler):

    def __init__(self):
        Compiler.__init__()
        self._executable = which('cc')
    
    def compile_files(self):
        counter = 0
        for file_name in self.__file_list:
            module = ''
            percentage = self.__percentage(counter, self.__file_list)
            out_file = file_name.split('/')
            subdir_list = out_file
            out_file = out_file.pop()
            subdir_list.pop()
            if not len(subdir_list) == 1:
                module = '/'.join(subdir_list)
            else:
                module = subdir_list.pop()
            self.__info_string(percentage, out_file)
            out_file = '{0}{1}'.format(out_file, '.o')
            run_string = '{0} -o {1} -c {2}'.format(
                    self.executable, out_file, self.__compile_flags)
            return_value = subprocess.call(run_string)
            if not return_value == 0:
                return return_value
            counter += 1
        return 0

    def link_files(self):
        pass

    def add_define(self, define):
        self.__compile_flags += format_options(flags, '-D')

    def add_include_directory(self, directory):
        self.__compile_flags += format_options(flags, '-I')

    def add_library_directory(self, directory):
        self.__link_flags += format_options(flags, '-L')

    def add_library(self, library):
        self.__link_flags += format_options(flags, '-l')

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        if isinstance(value, basestring):
            self._executable = which(value)

    @property
    def extensions(self):
        return ['.c']
