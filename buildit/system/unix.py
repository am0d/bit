# Basic Unix-Based C/C++ System
import os
import subprocess

from subprocess import Popen

from buildit.compiler.cc import CC
from buildit.system.system import System
from buildit.utils import error, flatten

class Unix(System):

    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = CC(project_name)
    
    def __str__(self):
        return 'Unix'

    def add_pkg(self, *scripts):
        scripts = flatten(list(scripts))
        for script in scripts:
            process = Popen(['{0}-config'.format(script), 
                         '--cflags', '--libs'], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, universal_newlines=True)
            output, errput = process.communicate()
            if not output:
                error('{0}: {1}'.format(package, errput))
                return
            output = output.replace('\n', ' ')
            self.compiler.add_compile_flags(output)
            self.compiler.add_link_flags(output)

    def pkg_config(self, *packages):
        packages = flatten(list(packages))
        for package in packages:
            process = Popen(['pkg-config', '{0}'.format(package), 
                         '--cflags', '--libs'], stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, universal_newlines=True)
            output, errput = process.communicate()
            if not output:
                error('{0}: {1}'.format(package,errput))
                return
            output = output.replace('\n', ' ')
            self.compiler.add_compile_flags(output)
            self.compiler.add_link_flags(output)

    def add_define(self, *defines):
        self.compiler.add_define(*defines)

    def add_include_directory(self, *directories):
        self.compiler.add_include_directory(*directories)

    def add_library_directory(self, *directories):
        self.compiler.add_library_directory(*directories)

    def add_library(self, *libraries):
        self.compiler.add_library(*libraries)

    def add_flag(self, *flags):
        self.compiler.add_flags(*flags)

    def add_link_flag(self, *flags):
        self.compiler.add_link_flags(*flags)

    @property
    def C99(self):
        self.compiler.C99

    @property
    def enable_c(self):
        self.compiler.enable_c
