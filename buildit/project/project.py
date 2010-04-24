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

        self.compiler_list = [Compiler]
        self.linker = Linker
        self.build_steps = [ ]
        self.file_list = [ ]
        
        self.build_steps.append(self.build)
        
        self.object_directory = 'object/{0}/{1}'.format(self.name, 
                self.project_name)
        self.output_directory = 'build/{0}/{1}'.format(self.name, 
                self.project_name)

        # Commandline options
        self.options = OptionGroup(buildit.parser, 'Project Specific Options:',
                                   'These will apply to *all* projects')
        self.options.add_option('-c', '--clean', action='store_true', 
                                dest='clean', default=False,
                                help='Removes the object files and build files')
        self.options.add_option('-r', '--rebuild', action='store_true',
                                dest='rebuild', default=False,
                                help='Fully rebuilds the project')
        buildit.parser.add_option_group(self.options)

    def __str__(self):
        return 'Project'

    def run(self):
        self.set_options()
        os.chdir(self.project_directory)
        start_time = datetime.now()
        for function in self.build_steps:
            return_value = function()
            if not return_value:
                error('Error: {0}'.format(return_value))
                sys.exit(return_value)
        end_time - datetime.now()
        info('{0}|{1}: {2}'.format(self.project_name.upper(), self.name,
                                   (end_time - start_time)))

    def build(self):
        object_list = [ ]
        if len(self.compiler_list > 0):
            for compiler in self.compiler_list:
                compiler_inst = compiler(self.project_name, self.file_list)
                compiler.object_directory = self.object_directory
                if not compiler_inst.run:
                    error('TEMP ERROR UNTIL NOT LAZY')
                object_list += compiler_inst.completed_files
        else:
            object_list = self.file_list
        linker = self.linker(self.project_name, self.project_type)
        linker.output_directory = self.output_directory
        linker.run(flatten(object_list))
        return 0 

    def append_step(self, function):
        self.build_steps.append(function)

    def prepend_step(self, function):
        self.build_steps.insert(function, 0)

    def insert_step(self, function, location):
        self.build_steps.insert(function, location)

    def is_complete(self):
        return self.project_complete

    def add_compiler(self, *compilers):
        compilers = flatten(compilers)
        for compiler in compilers:
            self.compiler_list.append(compiler)

    def add_directory(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            self.file_list.append(file_name)
        

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
            self.file_list.append(file_name)

    def remove_directory(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(clean_list(glob_list))
        for file_name in glob_list:
            try:
                self.file_list.remove(file_name)
            except ValueError:
                warning('{0} could not be removed.'.format(file_name))

    def remove_files(self, *files):
        files = flatten(files)
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
                self.file_list.remove(file_name)
            except ValueError:
                warning('{0} could not be removed.'.format(file_name))

    def require(self, required_system):
        self.build_steps.insert(0, required_system.run)

    def set_options(self):
        if buildit.options.rebuild:
            self.build_steps.insert(0, self.rebuild)

    def rebuild(self):
        database_path = '.buildit/{1}'.format(self.project_name)
        if os.path.exists(database_path):
            try:
                os.remove(database_path)
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
