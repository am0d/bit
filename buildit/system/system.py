# Base System Class

import os
import sys
import shutil
import threading
from glob import glob
from datetime import datetime
from optparse import OptionParser

from buildit.compiler.compiler import Compiler
from buildit.database import Database
from buildit.utils import lookup_error, flatten, fix_strings
from buildit.cprint import error, warning, info

class System(threading.Thread):

    def __init__(self, project_name):
        threading.Thread.__init__(self)
        self._compiler = Compiler(project_name)
        self.parser = OptionParser(conflict_handler='resolve')
        self._build_steps = []
        self._file_list = []
        self._project_name = project_name
        self._build_directory = ''
        self._object_directory = ''
        self._type = 'binary'
        self._complete = False

        self.build_directory = 'build/{0}'.format(self.name)
        self.object_directory = 'object/{0}/{1}'.format(project_name, 
                                self.name)

        self._build_steps.append(self.parse_deps)
        self._build_steps.append(self.build)
        

    def __str__(self):
        return 'System'

    def run(self):
        self.parse_options()
        start_time = datetime.now()
        for function in self._build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}: {1}'.format(self._project_name.upper(), 
            (end_time - start_time)))
        self._complete = True
        return 0

    def build(self):
        return self.compiler.run
        
    def append(self, function):
        self._build_steps.append(function)

    def prepend(self, function):
        self._build_steps.insert(function, 0) 

    def is_complete(self):
        return self._complete

    def add_path(self, *directories):
        path_list = []
        directories = flatten(list(directories))
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
            for extension in self.compiler.extensions:
                glob_list += glob('{0}/*{1}'.format(directory, extension))
            for file_name in glob_list:
                self._file_list.append(file_name)
        self._file_list.sort()
        self.compiler._file_list = self._file_list

    def add(self, *files):
        files = flatten(list(files))
        for file in files:
            if os.path.isdir(file):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extension in self.compiler.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    self._file_list.append(file_name)
            else:
                self._file_list.append(file)
        self._file_list.sort()
        self.compiler._file_list = self._file_list

    def remove(self, *files):
        files = flatten(list(files))
        for file in files:
            if os.path.isdir(file):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extension in self.compiler.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    try:
                        self._file_list.remove(file_name)
                    except ValueError:
                        warning('{0} could not be removed'.format(file_name))
            else:
                try:
                    self._file_list.remove(file)
                except ValueError:
                    warning('{0} could not be removed'.format(file))
        self._file_list.sort()
        self.compiler._file_list = self._file_list

    def require(self, required_system):
        self._build_steps.insert(0, required_system.run)

    def clean(self):
        clean_list = [self.object_directory, self.build_directory]
        for item in clean_list:
            if os.path.exists(item) and not item == '.':
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

    def parse_deps(self):
        return self.compiler.parse_deps()

    def rebuild(self):
        # Just delete the databases and everything should work out >:D
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0

    def change_base_directory(self, directory):
        os.chdir(directory)
        return 0

    def parse_options(self):
        self.parser.add_option('-c', '--clean', action='store_true', 
                               dest='clean', help='Cleans the project')
        self.parser.add_option('-r', '--rebuild', action='store_true', 
                               dest='rebuild', help='Rebuilds the project')
        self.parser.add_option('-n', '--no-deps', action='store_true', 
                               dest='no_deps', help='No dependency tracking')
        self.parser.add_option('-d', '--directory', dest='base_directory',
                               default='.', help='Changes the base directory')

        self.options, self.args = self.parser.parse_args()
        if self.options.parse_deps:
            try:
                self._build_steps.remove(self.parse_deps)
            except ValueError:
                error('Could not halt dependency tracking')
        if self.options.rebuild:
            self._build_steps.insert(0, self.rebuild)
        if self.options.clean:
            self._build_steps = [self.clean]
        self.change_base_directory(self.options.base_directory)

    def add_dependency_folder(self, *folders):
        self.compiler.add_dependency_folder(*folders)

    def add_file_extension(self, *extensions):
        self.compiler.add_file_extension(*extensions)

    def add_dependency_extension(self, *extensions):
        self.compiler.add_dependency_extension(*extensions)

    @property
    def static(self):
        self._type = 'static'
        self.compiler.type = self._type

    @property
    def dynamic(self):
        self._type = 'dynamic'
        self.compiler.type = self._type

    @property
    def binary(self):
        self._type = 'binary'
        self.compiler.type = self._type

    @property
    def name(self):
        return self.__str__()

    @property
    def compiler(self):
        return self._compiler

    # Currently broken in some instances
    @compiler.setter
    def compiler(self, value):
        self._compiler = value
        # Update the information we need to.
        self._compiler.object_directory = self._object_directory
        self._compiler.build_directory = self._build_directory
        self._compiler._file_list = self._file_list
        self._compiler.type = self._type
        self._compiler._project_name = self._project_name

    @property
    def build_directory(self):
        return self._build_directory

    @build_directory.setter
    def build_directory(self, value):
        self._build_directory = value
        self._compiler.build_directory = value

    @property
    def object_directory(self):
        return self._object_directory

    @object_directory.setter
    def object_directory(self, value):
        self._object_directory = value
        self._compiler.object_directory = value
