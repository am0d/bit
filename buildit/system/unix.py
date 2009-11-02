# Basic Unix-Based C/C++ System

from buildit.compiler.cc import CC
from buildit.system.system import System

class Unix(System):

    def __init__(self, project_name, unity_build=False):
        super().__init__(project_name, unity_build)
        self.compiler = CC()

    def add_define(self, define):
        self.compiler.add_define(define)

    def add_include_directory(self, directory):
        self.compiler.add_include_directory(directory)

    def add_library_directory(self, directory):
        self.compiler.add_library_directory(directory)

    def add_library(self, library):
        self.compiler.add_library(library)

    def add_flag(self, flag):
        self.compiler.add_flags(flag)
