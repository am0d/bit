# Windows Based C/C++ System (GCC BASED)

import os
import subprocess

from buildit.system.unix import Unix
from buildit.utils import which, flatten
from buildit.cprint import error

class MinGW(Unix):

    def __init__(self, project_name):
        Unix.__init__(self, project_name)
        self.compiler.executable = 'gcc'
        self.resource_compiler = 'windres'

    def __str__(self):
        return 'MinGW'

    def resource(self, *files):
        files = flatten(list(files))
        for file_name in files:
            directory = file_name.split('/')
            directory.pop()
            directory = '/'.join(directory)
            directory = '{0}/{1}'.format(self.object_directory, directory)
            try:
                os.makedirs(directory)
            except OSError:
                pass
            file_out = '{0}/{1}.o'.format(self.object_directory, file_name)
            run_string = '{0} {1} {2}'.format(self.resource_compiler, 
                file_name, file_out)
            try:
                return_value = subprocess.call(run_string) 
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                error('Could not compile resource file: {0}'.format(file_name))
                return
            self.compiler._link_list.append(file_out)

    @property
    def resource_compiler(self):
        return self.__resource_compiler

    @resource_compiler.setter
    def resource_compiler(self, value):
        self.__resource_compiler = which(value)
