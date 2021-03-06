# MinGW Class

import os
import subprocess

from bit.project.unix import Unix
from bit.utils import which, flatten
from bit.cprint import error

class MinGW(Unix):

    def __init__(self, project_name):
        Unix.__init__(self, project_name)
        self.resource_compiler = 'windres'
        self.compiler.executable = 'gcc'

    def __str__(self):
        return 'MinGW'

    def resource(self, *files):
        for file_name in flatten(list(set(files))):
            directory = file_name.split('/')
            directory.pop()
            directory = '/'.join(directory)
            directory = '{0}/{1}'.format(self.object_directory, directory)
            try:
                os.makedirs(directory)
            except OSError:
                pass
            file_out = '{0}/{1}.{2}'.format(self.object_directory, file_name, self.output_extension)
            run_string = '{0} {1} -o {2}'.format(self.resource_compiler, file_name, file_out)
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if return_value:
                return
            self.compiler.link_list.append(file_out)

    @property
    def CXX(self):
        self.executable = 'g++'

    @property
    def resource_compiler(self):
        return self.rc

    @resource_compiler.setter
    def resource_compiler(self, value):
        self.rc = which(value)
