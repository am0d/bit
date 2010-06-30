# MSVC Project Class

import os
import subprocess

from bit.project.project import Project
from bit.compiler.msvc import MSVCCompiler
from bit.utils import fix_strings, which

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
        # Now here's where the magic happens
        if not os.path.exists('.bit/msvc.bat'):
            with open('.bit/msvc.bat', 'w') as file:
                file.write('@call "{0}/vcvarsall.bat" {1}'.format(msvc_path, self.arch))
                file.write('\n@echo %PATH%')
        os.chdir('.bit')
        syscheck = subprocess.Popen('msvc.bat', stdout=subprocess.PIPE, universal_newlines=True).communicate()
        os.chdir('..')
        syscheck = list(syscheck).pop(0).split('\n').pop(1)
        syscheck = fix_strings([path for path in syscheck.split(os.pathsep)])
        os.environ['PATH'] = os.pathsep.join(syscheck)
        return 0

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
    
