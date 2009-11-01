# Unix Based C Compiler

import os
import shutil

from buildit.compiler.compiler import Compiler
from buildit.utils import which
from buildit.cprint import command

class CC(Compiler):
    
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

    def link_files(self):
        pass

    def add_define(self, define):
        self.__flags += format_options(flags, '-D')

    def add_include_directory(self, directory):
        self.__flags += format_options(flags, '-I')

    def add_library_directory(self, directory):
        self.__flags += format_options(flags, '-L')

    def add_library(self, library):
        self.__flags += format_options(flags, '-l')

    @property
    def executable(self):
        return which('cc')

    @property
    def extensions(self):
        return ['.c']
