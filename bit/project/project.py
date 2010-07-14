# Base "Project" Class

import os
import sys
import shutil
import threading

from glob import glob
from datetime import datetime
from optparse import OptionGroup

from bit.instance import bit

from bit.utils import flatten, fix_strings
from bit.cprint import success, warning, error, info

from bit.compiler.compiler import Compiler

class Project(threading.Thread):

    def __init__(self, project_name):
        threading.Thread.__init__(self)
        self.project_name = project_name
        self.project_directory = '.'
        self.project_type = 'binary'
        self.project_complete = False

        self.compiler = Compiler(self.project_name)
        self.build_steps = [ ]
        self.file_list = [ ]
        
        self.build_steps.append(self.build)

        self.output_directory = 'build/{0}/{1}'.format(self.name, self.project_name)
        self.object_directory = '.bit/{0}'.format(self.project_name)
        # Commandline options
        self.options = OptionGroup(bit.parser, 'Project Specific Options:',
                                   'These will apply to *all* projects')
        self.options.add_option('-r', '--rebuild', action='store_true',
                                dest='rebuild', default=False,
                                help='Fully rebuilds the project')
        bit.parser.add_option_group(self.options)
        try:
            os.makedirs('.bit')
        except OSError:
            pass

    def __str__(self):
        return 'Project'

    def run(self):
        self.set_options()
        os.chdir(self.project_directory)
        start_time = datetime.now()
        for function in self.build_steps:
            return_value = function()
            if not return_value == 0: # This line breaks so much I HAD to put in the == 0 :/
                error('Error: {0}'.format(return_value))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}|{1}: {2}'.format(self.name.upper(), self.project_name, (end_time - start_time)))
        return 0

    def build(self):
        self.compiler.file_list = self.file_list
        self.compiler.build_directory =self.output_directory
        if self.compiler.run:
            return 1
        self.project_complete = True
        return 0 

    def append_step(self, function):
        self.build_steps.append(function)

    def prepend_step(self, function):
        self.build_steps.insert(0, function)

    def insert_step(self, function, location):
        self.build_steps.insert(location, function)

    def is_complete(self):
        return self.project_complete

    def directory(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(list(set(glob_list)))
        for file_name in glob_list:
            self.file_list.append(file_name)

    def files(self, *files):
        files = flatten(files)
        glob_list = [ ]
        for file_name in files:
            if os.path.isdir(file_name):
                for root, directory, file_names in os.walk(file_name):
                    glob_list += glob('{0}/*'.format(root))
            else:
                glob_list.append(file_name)
        glob_list = fix_strings(list(set(glob_list)))
        for file_name in glob_list:
            self.file_list.append(file_name)
        

    def rmdir(self, *directories):
        directories = flatten(directories)
        glob_list = [ ]
        for directory in directories:
            glob_list += glob('{0}/*'.format(directory))
        glob_list = fix_strings(list(set(glob_list)))
        for file_name in glob_list:
            try:
                self.file_list.remove(file_name)
            except ValueError:
                raise Exception('Could not remove {0}'.format(file_name)) 

    def rmfiles(self, *files):
        files = flatten(files)
        glob_list = [ ]
        for file_name in files:
            if os.path.isdir(file_name):
                for root, directory, files_names in os.walk(file):
                    glob_list += glob('{0}/*'.format(root))
            else:
                glob_list.append(file_name)
        glob_list = fix_strings(list(set(glob_list)))
        for file_name in glob_list:
            try:
                self.file_list.remove(file_name)
            except ValueError:
                raise Exception('Could not remove {0}'.format(file_name)) 

    def require(self, required_system):
        self.build_steps.insert(0, required_system.run)

    def set_options(self):
        if bit.options.rebuild:
            self.build_steps.insert(0, self.rebuild)

    def rebuild(self):
        database_path = '.bit/{0}'.format(self.project_name)
        if os.path.exists(database_path):
            try:
                shutil.rmtree(database_path)
            except OSError:
                error('Could not remove database/configuration folder!')
        else:
            warning('No database folder found.')
        return 0

    @property
    def name(self):
        return self.__str__()

    @property
    def static(self):
        self.project_type = 'static'
        self.compiler.type = self.project_type

    @property
    def binary(self):
        self.project_type = 'binary'
        self.compiler.type = self.project_type

    @property
    def dynamic(self):
        self.project_type = 'dynamic'
        self.compiler.type = self.project_type
