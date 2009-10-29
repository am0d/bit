# Base Linker Class

import os
import subprocess
import glob

from buildit.utils import which, format_options
from buildit.utils import name
from buildit.cprint import command

class Linker(object):
    
    def __init__(self):
        self.__file_list = []
        self.__link_steps = []
        self.__flags = ''
        self.__link_steps.append(self.link)

        self.__output_option = '>'
        self.__source_option = '<'

        self.__object_dir = ''
        self.__build_dir = '.'
        self.__target = 'a.out'
        
    def run(self, unity_build):
        print 'Linking ...'
        for function in self.__link_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def link(self):
        infiles = '{0}/*.{1}'.format(self.__object_dir, self.__extensions)
        outfile_name = '{0}/{1}'.format(self.__build_dir, self.__target)

        command('{0}: {1}'.format(self.name.upper(), outfile_name))
        run_string = '{0} {1} {2} {3} {4}'.format(self.exe,
                        self.__output_option, outfile_name,
                        self.__source_option, infile_name)
        try:
            subprocess.call(run_string)
        except OSError:
            os.system(run_string)
    
    @property
    def name(self):
        return name(self)
    
    def add_flags(self, flags):
        self.__flags += flags

    @property
    def exe(self):
        return which('echo')
    
    @property    
    def extensions(self):
        return ['.txt']
        
    @property
    def object_dir(self):
        return self.__object_dir

    @object_dir.setter
    def object_dir(self, dir):
        self.__object_dir = dir

    @property
    def build_dir(self):
        return self.__build_dir

    @build_dir.setter
    def build_dir(self, dir):
        self.__build_dir = dir
    
    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target
