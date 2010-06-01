# Basic Unix Program

import os
import subprocess

from bit.project.project import Project
from bit.compiler.cc import CC
from bit.utils import flatten

class Unix(Project):

    def __init__(self, project_name):
        Project.__init__(self, project_name)
        self.compiler = CC(self.project_name)
        self.output_extension = self.compiler.output_extension

    def __str__(self):
        return 'Unix'

    def pkg(self, *scripts):
        for script in flatten(list(set(scripts))):
            cflags = config_script_flags(script, '', '--cflags')
            lflags = config_script_flags(script, '', '--libs')
            self.compiler.cflags(cflags)
            self.compiler.lflags(cflags, lflags)

    def pkg_config(self, packages):
        for package in flatten(list(set(packages))):
            cflags = config_script_flags('pkg', package, '--cflags')
            lflags = config_script_flags('pkg', package, '--libs')
            self.compiler.cflags(cflags)
            self.compiler.lflags(cflags, lflags)

    def define(self, *defines):
        self.compiler.define(defines)

    def incdir(self, *directories):
        self.compiler.incdir(directories)

    def libdir(self, *directories):
        self.compiler.libdir(directories)

    def library(self, *libraries):
        self.compiler.library(libraries)

    def cflags(self, *flags):
        self.compiler.cflags(flags)

    def lflags(self, *flags):
        self.compiler.lflags(flags)
    
    def flags(self, *flags):
        self.compiler.cflags(flags)
        self.compiler.lflags(flags)

    @property
    def C99(self):
        self.compiler.C99

    @property
    def CXX(self):
        self.compiler.CXX

    @property
    def CPP(self):
        self.compiler.CXX

    @property
    def enable_c(self):
        self.compiler.enable_c

def config_script_flags(script, package, argument):
    process = subprocess.Popen(['{0}-config'.format(script), package, argument], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    output, errput = process.communicate()
    if output == None:
        raise Exception('Config error!\n{0}: {1}'.format(package, errput))
    return output.replace('\n', '')
