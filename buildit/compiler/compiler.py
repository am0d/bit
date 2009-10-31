#Base Compiler Class

import os
import subprocess

from buildit.utils import which
from buildit.utils import flatten
from buildit.utils import fix_strings
from buildit.utils import name as uname
from buildit.cprint import command

class Compiler(object):
    
    def __init__(self):
        self.__file_list = []
        self.__compile_steps = []
        self.__flags = ''
        self.__type = '' # Added for much much later on
        self.__object_dir = '.'

        self.__compile_steps.append(self.setup_files)
        self.__compile_steps.append(self.compile_files)
        self.__compile_steps.append(self.link_files)

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
            os.makedirs(self.__object_dir)
        except:
            pass
        return 0

    # Leave the implementation up to each compiler
    def compile_files(self):
        pass

    def link_files(self):
        pass

    def __percentage(self, counter, file_list):
        ''' 
            Calculates the percentage of files completed, and returns it as a
            string 
        '''
        percentage = 100 * float(counter)/float(len(file_list))
        percentage = str(percentage).split('.')
        percentage = percentage.pop(0)
        return percentage

    def __info_string(self, percentage, file_name):
        ''' Prints out what file is being created '''
        command('[{0:>3}%] {1}: {2}'.format(percentage, self.name.upper(), file_name))

    def add_flags(self, flags):
        self__flags += format_options(flags)

    @property
    def executable(self):
        return which('echo')

    @property
    def output_extension(self):
        return '.txt'

    @property
    def object_directory(self):
        return self.__object_directory

    @object_directory.setter
    def object_directory(self, value):
        self.__object_directory = value

    @property
    def extensions(self):
        return ['.txt']

    @property
    def name(self):
        return uname(self)
