# Basic Unix-Based C/C++ System

import commands

from buildit.compiler.cc import CC
from buildit.system.system import System
from buildit.utils import error

class Unix(System):

    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = CC(project_name)

    def pkg_config(self, package, script='pkg'):
        if not script == 'pkg':
            package = ''
        config = commands.getstatusoutput('{0}-config --cflags {1}'.format(
            script, package))
        config = list(config)
        return_value = config.pop(0)
        if not return_value == 0:
            error('Could not add {0} to configuration'.format(package))
        else:
            self.compiler.add_compile_flags(config.pop())
        # Some CFlags need to be passed to the linker.
        conf = '{0}-config --cflags --libs {1}'.format(script, package)
        config = commands.getstatusoutput(conf)
        config = list(config)
        return_value = config.pop(0)
        if not return_value == 0:
            error('Could not add {0} to configuration'.format(package))
        else:
            self.compiler.add_link_flags(config.pop())


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

    def add_link_flag(self, flag):
        self.compiler.add_link_flags(flag)

    @property
    def C99(self):
        self.compiler.C99

    @property
    def enable_c(self):
        self.compiler.enable_c
