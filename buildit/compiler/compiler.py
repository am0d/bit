# Base Compiler Class

from buildit.utils import which
from buildit.cprint import command

class Compiler(object):

    def __init__(self):
        self.name = self.name()
        self.exe = self.exe()
        self.extensions = self.extensions()
        self.__flags = ''
        self.__file_list = []
        self.compile_steps = []
        
        self.compile_steps.append(self.setup_files)
        self.compile_steps.append(self.compile_files)

    def run(self, unity_build):
        for function in self.compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def setup_files(self):
        self.file_list = flatten(self.file_list)
        self.file_list = fix_strings(self.file_list)
        for file_name in self.file_list:
            for extension in self.extensions:
                if not file_name.endswith(extension):
                    self.file_list.remove(file_name)
        return 0
        
    def compile_files(self):
        command('{0}: {1}'.format(self.name.upper(), outfile_name))
        return 0 #; Go away semi-colon, no one loves you!

    def add_flags(self, flags):
        self.__flags += format_options(flags)

    def exe(self):
        return which('echo')
        
    def extensions(self):
        return ['.txt']

    def name(self):
        name = str(self)
        name = name.split('(')
        name = name.pop(0)
        name = name.replace('<', '')
        name = name.replace('\n', '')
        return name
