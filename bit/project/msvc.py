# MSVC Project Class

import subprocess

from bit.project.project import Project
from bit.utils import fix_strings

class MSVC(Project):
    
    def __init__(self, project_name):
        Project.__init__(self, project_name)
        self.arch = 'x86'
        self.prepend_step(

    def __str__(self):
        return 'MSVC'

    def setup_environment(self):
        msvc_path = fix_strings([os.environ[self.compiler_version]]).pop().split('/')
        msvc_path.pop(), msvc_path.pop()
        return subprocess.call('{0}/{1} {2}'.format(msvc_path, vcvarsall.bat, self.arch))

    def add_define(self, *defines):
        self.compiler.add_define(defines)

    def add_library(self, *libraries):
        self.compiler.add_library(libraries)

    def add_library_directory(self, *directories):
        self.compiler.add_library_directory(directories)

    def add_include_directory(self, *directories):
        self.compiler.add_include_directory(directories)

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
    
