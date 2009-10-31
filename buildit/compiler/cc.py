# Unix Based C Compiler

import os
import shutil

from buildit.compiler.compiler import Compiler
from buildit.utils import which
from buildit.cprint import command

class CC(Compiler):
    
    def compile_files(self):
        pass

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
