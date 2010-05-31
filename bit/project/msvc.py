# MSVC Project Class

import os
import subprocess

from bit.project.project import Project
from bit.compiler.msvc import MSVCCompiler
from bit.utils import fix_strings

from bit.cprint import error

class MSVC(Project):
    
    def __init__(self, project_name):
        Project.__init__(self, project_name)
        self.compiler = MSVCCompiler(self.project_name)
        self.vs2008 # We'll try 2008 by default.
        self.arch = 'x86'
        self.prepend_step(self.setup_environment)

    def __str__(self):
        return 'MSVC'

    def setup_environment(self):
        msvc_path = fix_strings([os.environ[self.compiler_version]]).pop().split('/')
        msvc_path.pop(), msvc_path.pop(), msvc_path.pop()
        msvc_path.append('VC')
        msvc_path = '/'.join(msvc_path)
        ret_value = subprocess.call('{0}/vcvarsall.bat {1}'.format(msvc_path, self.arch))
        
        return ret_value

    def define(self, *defines):
        self.compiler.define(defines)

    def incdir(self, *directories):
        self.compiler.incdir(directories)

    def libdir(self, *directories):
        self.compiler.libdir(directories)

    def library(self, *libraries):
        self.compiler.library(libraries)

    def flag(self, *flags):
        self.compiler.flags(flags)

    def lflag(self, *flags):
        self.compiler.lflags(flags)
    
    # Compatibility :)
    @property
    def CXX(self):
        pass

    @property
    def x64(self):
        self.arch = 'x64'

    @property
    def vs2010(self):
        self.compiler_version = 'VS100COMNTOOLS'

    @property
    def vs2008(self):
        self.compiler_version = 'VS90COMNTOOLS'
    
    @property
    def vs2005(self):
        self.compiler_version = 'VS80COMNTOOLS'
    
