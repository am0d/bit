# Base Linker Class

import os
import subprocess

from buildit.utils import which, format_options
from buildit.cprint import command

class Linker(object):
    
    def __init__(self):
        self.__name = self.name()
        self.exe = self.exe()
        self.extensions = self.extensions()
        self.__file_list = []
        self.__link_steps = []
        self.__flags = ''
        
        self.link_steps.append(self.link)
        
    def run(self, unity_build):
        for function in self.link_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def link(self):
        command('{0}: {1}'.format(self.name.upper(), outfile_name))
        try:
            subprocess.call(run_string)
        except OSError:
            os.system(run_string)
    
    def name(self):
        name = str(self)
        name = name.split('(')
        name = name.pop(0)
        name = name.replace('<', '')
        name = name.replace('\n', '')
        return name
    
    def add_flags(self, flags):
        self.__flags += flags

    @property
    def exe(self):
        return which('echo')
    
    @property    
    def extensions(self):
        return ['.txt']
        
    
