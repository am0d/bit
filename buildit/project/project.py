# Base "Project" Class

import os
import sys
import shutil
import threading

from glob import glob
from datetime import datetime
from optparse import OptionGroup

import buildit.buildit as buildit

from buildit.utils import flatten, fix_strings, clean_list
from buildit.cprint import success, warning, error, info

from buildit.compiler.compiler import Compiler
from buildit.linker.linker import Linker

class Project(threading.thread):

    def __init__(self, project_name):
        threading.Thread.__init__(self)
        self.project_name = project_name
        self.project_directory = '.'
        self.project_type = 'binary'
        self.project_complete = False

        self._compiler_list = [Compiler]
        self.__build_steps = [ ]
        self._file_list = [ ]
        
        self.__build_steps.append(self.build)

        # Commandline options
        self.options = OptionGroup(buildit.parser, 'Project Specific Options:',
                                   'These will apply to *all* projects')
        self.options.add_option('-c', '--clean', action='store_true', 
                                dest='clean',
                                help='Removes the object files and build files')
        self.options.add_option('-r', '--rebuild', action='store_true',
                                dest='rebuild',
                                help='Fully rebuilds the project')
        buildit.parser.add_option_group(self.options)

    def __str__(self):
        return 'Project'

    def run(self):
        self.set_options()
        os.chdir(self.project_directory)
        start_time = datetime.now()
        for function in self.__build_steps:
            return_value = function()
            if not return_value:
                error('Error: {0}'.format(return_value))
                sys.exit(return_value)
        end_time - datetime.now()
        info('{0}|{1}: {2}'.format(self.project_name.upper(), self.name,
                                   (end_time - start_time)))

    def build(self):
        object_list = [ ]
        for compiler in self._compiler_list:
            compiler_inst = compiler(self.project_name, self._file_list)
            object_list += compiler.run
        linker = Linker(self.project_name)
        linker.run(object_list)
        return 0 #TODO: Add a bit more to this (Linker, etc.) 

    def append_step(self, function):
        self.__build_steps.append(function)

    def prepend_step(self, function):
        self.__build_steps.insert(function, 0)

    def insert_step(self, function, location):
        self.__build_steps.insert(function, location)

    def is_complete(self):
        return self.project_complete

    def add_compiler(self, *compilers):
        compilers = flatten(compilers)
        for compiler in compilers:
            self._compiler_list.append(compiler)

    def add_directory(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            self._file_list.append(file_name)
        

    def add_files(self, *files):
        files = flatten(files)
        glob_list = [ ]
        for file_name in files:
            if os.path.isdir(file_name):
                for root, directory, file_names in os.walk(file):
                    glob_list += glob('{0}/*'.format(root))
            else:
                glob_list.append(file_name)
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            self._file_list.append(file_name)

    def remove_directory(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            try:
                self._file_list.remove(file_name)
            except ValueError:
                warning('{0} could not be removed.'.format(file_name))

    def remove_files(self, *files):
        files = flatten(files))
        glob_list = [ ]
        for file_name in files:
            if os.path.isdir(file_name):
                for root, directory, files_names in os.walk(file):
                    glob_list += glob('{0}/*'.format(root))
            else:
                glob_list.append(file_name)
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            try:
                self._file_list.remove(file_name)
            except ValueError:
                warning('{0} could not be removed.'.format(file_name))

    def require(self, required_system):
        self.__build_steps.insert(0, required_system.run)

    def set_options(self):
        if buildit.options.rebuild:
            self.__build_steps.insert(0, self.rebuild)

    def rebuild(self):
        if os.path.exists('.buildit'):
            try:
                os.remove('.buildit')
            except:
                error('Could not remove database/configuration folder!')
        else:
            warning('No database folder found.')

    @property
    def name(self):
        return self.__str__()

    @property
    def static(self):
        self.project_type = 'static'

    @property
    def binary(self):
        self.project_type = 'binary'

    @property
    def dynamic(self):
        self.project_type = 'dynamic'
