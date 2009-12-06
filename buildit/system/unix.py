# Basic Unix-Based C/C++ System
import os
import subprocess

from subprocess import Popen

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
        process = Popen('{0}-config {1} --cflags'.format(script, package), 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errput = process.communicate()
        if not output:
            error('{0}: {1}'.format(package,errput))
            return
        output = output.replace('\r\n', '')
        self.compiler.add_compile_flags(output)
        # Some CFlags need to be passed to the linker.
        process = Popen('{0}-config {1} --cflags --libs'.format(script, package), 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errput = process.communicate()
        if not output:
            error('{0}: {1}'.format(package,errput))
            return
        output = output.replace('\r\n', '')
        self.compiler.add_link_flags(output)


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
