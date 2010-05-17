# Basic Unix Program

import os
import subprocess

from bit.project.project import Project
from bit.compiler.gcc import GCC
from bit.utils import flatten
from bit.cprint

class Unix(Project):

    def __init__(self, project_name):
        Project.__init__(self, project_name)
        self.compiler = GCC(self.project_name)

    def __str__(self):
        return 'Unix'

    def add_pkg(self, *scripts):
        for script in flatten(list(set(scripts))):
            cflags = config_script_flags(script, '', '--cflags')
            lflags = config_script_flags(script, '', '--libs')
            self.compiler.add_compile_flags(cflags)
            self.compiler.add_link_flags(cflags, lflags)

    def pkg_config(self, (packages):
        for package in flatten(list(set(packages))):
            cflags = config_script_flags('pkg', package, '--cflags')
            lflags = config_script_flags('pkg', package, '--libs')
            self.compiler.add_compile_flags(cflags)
            self.compiler.add_link_flags(cflags, lflags)

    def add_define(self, *defines):
        self.compiler.add_define(defines)

    def add_include_directory(self, *directories):
        self.compiler.add_include_directory(directories)

    def add_library_directory(self, *directories):
        self.compiler.add_library_directory(directories)

    def add_library(self, *libraries):
        self.compiler.add_library(libraries)

    def add_flag(self, *flags):
        self.compiler.add_flags(flags)

    def add_link_flag(self, *flags):
        self.compiler.add_link_flags(flags)

    @property
    def C99(self):
        self.compiler.C99

    @property
    def CXX(self):
        self.compiler.CXX

    @property
    def CPP(self):
        self.compiler.CXX

def config_script_flags(script, package, argument):
    process = subprocess.Popen(['{0}-config'.format(script), package, argument], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    output, errput = process.communicate()
    if not output:
        error('{0}: {1}'.format(package, errput))
        return
    return output.replace('\n', '')
