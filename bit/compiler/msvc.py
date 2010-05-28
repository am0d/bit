# MSVC Compiler

from bit.compiler.compiler import Compiler
from bit.utils import flatten, hash
from bit.cprint import command

class MSVCCompiler(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)

    def compile_files(self):
        pass

    def link_files(self):
        pass

    def define(self, *defines):
        for define in flatten(list(set(defines))):
            self.cflags('/D', define)

    def incdir(self, *directories):
        for directory in flatten(list(set(directories))):
            self.cflags('/I', directory)

    def libdir(self, *directories):
        for directory in flatten(list(set(directories))):
            self.lflags('/L', directory)

    def library(self, *libraries):
