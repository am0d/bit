# MSVC Compiler

import os

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
        path_list = [path for path in os.environ['LIB'].split(os.pathsep)]
        for directory in flatten(list(set(directories))):
            path_list.append(directory)
        os.environ['LIB'] = os.pathsep.join(path_list)

    def library(self, *libraries):
        for library in flatten(list(set(directories))):
            self.lflags('{0}.lib'.format(library))
