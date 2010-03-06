# Base System Class

import os
import sys
import shutil
import multiprocessing

from glob import glob
from datetime import datetime
from optparse import OptionParser

from buildit.compiler.compiler import Compiler
from buildit.database import Database

from buildit.utils import lookup_error, flatten, fix_strings, clean_list
from buildit.cprint import error, warning, info

class Platform(multiprocessing.Process):
    
    # Builtin Functions
    def __init__(self, project_name):
        multiprocessing.Process.__init__(self)
        self.parser = OptionParser(conflict_handler='resolve')
        self.project_name = project_name
        self.job_limit = 1
        self.build_directory = 'build/{0}'.format(self.name)
        self.object_directory = 'object/{0}/{1}'.format(self.project_name, 
                                  self.name)

        self._compiler = Compiler()
        self._build_steps = []
        self._file_list = [] # Primary File List
        self._type = 'binary'
        self._complete = False
        
        self._build_steps.append(self.parse_deps)
        self._build_steps.append(self.build)

    def __unicode__(self):
        return u'{0}'.format(self.__str__())

    def __str__(self):
        return 'Platform'

    def run(self):
        self.parse_options()
        start_time = datetime.now()
        for function in self._build_steps:
            return_value = function()
            if not return_value:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0|{1}: {2}'.format(self.project_name.upper(), self.name
                                  (end_time - start_time)))
        self._complete = True
        return 0

    def build(self): pass
        # TODO Write this function

    # Build Steps
    def append_step(self, function):
        self._build_steps.append(function)

    def prepend_step(self, function):
        self._build_steps.insert(function, 0)

    def insert_step(self, function, location):
        self._build_steps.insert(function, location)

    # Status
    def is_complete(self):
        return self._complete

    # Adding Items 
    def add_path(self, *directories):
        path_list = []
        directories = faltten(list(directories))
        for path in os.environ['PATH'].split(os.pathsep):
            path_list.append(path)
        for directory in directories:
            path_list.append(directory)
        path_list = os.pathsep.join(path_list)
        os.environ['PATH'] = path_list

    def add_directory(self, *directories):
        directories = flatten(list(directories))
        for directory in directories:
            glob_list = []
            for extension in self._compiler.extensions:
                glob_list += glob('{0}/*{1}'.format(directory, extension))
            for file_name in glob_list:
                self._file_list.append(file_name)
        clean_list(self._file_list)

    def add_files(self, *files):
        self.add(files)

    def add(self, *files):
        files = flatten_list(files))
        for file_name in files:
            if os.path.isdir(file_name):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extension in self._compiler.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    self._file_list.append(file_name)
            else:
                self._file_list.append(file)
        clean_list(self._file_list)

    #def add_file_extension Where should file extensions be placed?

    def remove(self, *files):
        files = flatten(list(files))
        for file_name in files:
            if os.path.isdir(file_name):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extension in self._compiler.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    try:
                        self._file_list.remove(file_name)
                    except ValueError:
                        warning('{0} could not be removed'.format(file_name))
            else:
                try:
                    self._file_list.remove(file_name)
                except ValueError:
                    warning('{0} could not be removed'.format(file_name))
        clean_list(self._file_list)

    def require(self, required_system):
        self._build_steps.insert(0, required_system.run)

    # Runtime options
    def clean(self):
        clean_list = [self.object_directory, self.build_directory]
        for item in clean_list:
            if os.path.exists(item) and not item == os.getcwd():
                try:
                    shutil.rmtree(item)
                except OSError:
                    pass
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0

    def rebuild(self):
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0

    def change_directory(self, directory):
        os.chdir(directory)
        return 0
    
    def parse_options(self):
        self.parser.add_option('-c', '--clean', action='store_true',
                               dest='clean', help='Cleans the project')
        self.parser.add_option('-r', '--rebuild', action='store_true',
                               dest='rebuild', help='Rebuilds the project')
        self.parser.add_option('-d', '--directory', dest='base_directory',
                               default='.', help='Changes the base directory')
        self.parser.add_option('-j', '--jobs', dest='job_limit', default=1,
                               help='Number of simultaneous jobs per project')

        self.options, self.args = self.parser.parse_args()
        if self.options.rebuild:
            self._build_steps.insert(0, self.rebuild)
        if self._build_steps.clean:
            self._build_steps = [self.clean]
        self.job_limit = self.options.job_limit
        if self.job_limit:
            self.job_limit = 1
        self.change_directory(self.options.base_directory)

    # Properties
    @property
    def name(self):
        return self.__unicode__()

    @property
    def static(self):
        self._type = 'static'

    @property
    def binary(self):
        self._type = 'binary'

    @property
    def dynamic(self):
        self._type = 'dynamic'

    @property
    def compiler(self):
        return self._compiler

    @compiler.setter
    def compiler(self, value):
        self._compiler = value
