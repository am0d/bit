# Base Linker Class

from buildit.utils import which
from buildit.cprint import command

class Linker(object):
    
    def __init__(self):
        self.name = self.name()
        self.exe = self.exe()
        self.extensions = self.extensions()
        self.file_list = []
        self.link_steps = []
        self.flags = ''
        
        self.link_steps.append(self.link)
        
    def run(self):
        for function in self.link_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def link(self):
        command('{0}: {1}'.format(self.name.upper(), outfile_name))
    
    def exe(self):
        return which('echo')
        
    def extensions(self):
        return ['.txt']
