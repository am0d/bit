# MSVC Compiler

from bit.compiler.compiler import Compiler

class MSVCCompiler(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)

    def compile_files(self):
        pass

    def link_files(self):
        pass

    def define(self, *defines):
        pass

    def incdir(self, *directories):
        pass

    def libdir(self, *directories):
        pass

    def library(self, *libraries):
        pass

    def flags(self, *flags):
        pass

    def lflags(self, *flags):
        pass
