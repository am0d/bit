# Base Linker Class

import subprocess

from buildit.utils import which

class Linker(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.file_list = [ ]
        self.linker_flags = [ ]
        self.linker_executable = which('echo')
        self.project_type = 'generic'

    # Override the run for each "linker"
    # Make sure it returns 0 on no error, and sets the file_list to 
    # self.file_list
    def run(self, file_list):
        self.file_list = file_list
        return 0

    def add_linker_flags(self, *flags):
        for item in flags:
            self.link_flags.append(item)

    @property
    def executable(self):
        return self.linker_executable

    @executable.setter
    def executable(self, value):
        self.linker_executable = which(value)

    @property
    def dynamic(self):
        self.project_type = 'dynamic'

    @property
    def static(self):
        self.project_type = 'static'

    @property
    def binary(self):
        self.project_type = 'binary'
