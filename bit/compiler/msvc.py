# MSVC Compiler

from bit.compiler.compiler import Compiler

class MSVCCompiler(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)

    def add_define(self, *defines):
        pass

    def add_library(self, *libraries):
        pass

    def add_library_directories(self, *directories):
        pass

    def add_include_directory(self, *directories):
        pass

    
