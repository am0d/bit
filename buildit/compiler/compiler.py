# Base Compiler Class

from buildit.utils import which
from buildit.cprint import command

class Compiler(object):

    def __init__(self):
        self.name = name()
        self.exe = self.exe()
        self.extensions = self.extensions()
        self.file_list = []
        self.flags = ''
        self.compile_steps = []
        
        self.compile_steps.append(setup_files)
        self.compile_steps.append(compile_files)

    def run(self):
        for function in self.compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def setup_files(self, file_list):
        file_list = flatten(file_list)
        file_list = fix_strings(file_list)
        for file_name in file_list:
            for extension in self.extensions:
                if not file_name.endswith(extension):
                    file_list.remove(file_name)
        return 0
        
    def compile_files(self):
        command('{0}: {1}'.format(self.name.upper(), outfile_name)
        
    def add_flags(self, flags):
        self.flags += format_options(flags)

    def exe(self, executable):
        return which('echo')
        
    def extensions(self, executable):
        return ['.txt']

    def name(self):
        name = str(self)
        name = name.split('(')
        name = name.pop(0)
        name = name.replace('<', '')
        name = name.replace('\n', '')
        return name
