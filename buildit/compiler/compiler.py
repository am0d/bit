# Base Compiler Class

import subprocess
import os

from buildit.utils import which
from buildit.utils import flatten
from buildit.utils import fix_strings
from buildit.cprint import command

class Compiler(object):

    def __init__(self):
        self.__flags = ''
        self.__file_list = []
        self.__compile_steps = []
        self.__object_dir = '.'

        self.__source_option = '-c'
        self.__output_option = '-o'
        
        self.__compile_steps.append(self.setup_files)
        self.__compile_steps.append(self.compile_files)

    def run(self, file_list, unity_build):
        self.__file_list = file_list
        for function in self.__compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def setup_files(self):
        self.__file_list = flatten(self.__file_list)
        self.__file_list = fix_strings(self.__file_list)
        for file_name in self.__file_list:
            for extension in self.extensions:
                if not file_name.endswith(extension):
                    self.__file_list.remove(file_name)

        try: 
            os.makedirs(self.__object_dir):
        except:
            pass
        return 0

    def compile_files(self):
        counter = 0
        for file_name in self.__file_list:
            out_file = file_name.split('/')
            out_file = out_file.pop()
            out_file = '{0}/{1}{2}'.format(self.__object_dir, out_file, 
                        self.output_extension)
            command('{0}: {1}'.format(self.name.upper(), out_file))
            run_string = '{0} {1} {2} {3} {4}'.format(self.exe, 
                    self.__source_option, file_name, 
                    self.__output_option, out_file) # TODO: FIX THIS. 
            try: 
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            counter +=1    
        return 0 #; Go away semi-colon, no one loves you!

    def add_flags(self, flags):
        self.__flags += format_options(flags)

    @property
    def exe(self):
        return which('echo')
        
    @property
    def output_extension(self):
        return '.txt'

    @property
    def object_directory(self):
        return self.__object_directory

    @object_dir.setter
    def object_directory(self, value):
        self.__object_directory = value
        
    @property    
    def extensions(self):
        return ['.txt']

    @property
    def name(self):
        return utils.name(self)
