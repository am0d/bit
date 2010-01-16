# Base System Class

import os
import gc
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
        self._build_steps = []
        self._file_list = []
        self._project_name = project_name
        self._build_directory = ''
        self._object_directory = ''
        self._type = 'binary'
        if not gc.isenabled():
            gc.enable()

        self.build_directory = 'build/{0}'.format(self.name)
        self.object_directory = 'object/{0}'.format(self.name)

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
        return 0

    def build(self):
        return_value = self.compiler.run
        return return_value

    def append(self, function):
        self._build_steps.append(function)

    def prepend(self, function):
        self._build_steps.insert(function, 0)

    def pause(self):
        raw_input('Press Enter to continue...')

    def add_path(self, *directories):
        path_list = []
        directories = list(directories)
        for path in os.environ['PATH'].split(os.pathsep):
            path_list.append(path)
        for directory in directories:
            path_list.append(directory)
        path_list = os.pathsep.join(path_list)
        os.environ['PATH'] = path_list

    def add(self, *files):
        files = flatten(list(files))
        for file in files:
            if os.path.isdir(file):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extension in self.compiler.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension)
                if sys.platform == 'win32':
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
                        glob_list += glob('{0}/*{1}'.format(root, extension)
                if sys.platform == 'win32':
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
        return 0

    def rebuild(self):
        if os.path.exists('.buildit'):
            try:
                shutil.rmtree('.buildit')
            except OSError:
                pass
        return 0

    def change_base_directory(self, directory):
        return 0

    def parse_options(self):
        self.parser = OptionParser()
        self.parser.add_option('--clean', action='store_true', dest='clean',
                               help='Cleans the project')
        self.parser.add_option('--rebuild', action='store_true', dest='rebuild',
                               help='Rebuilds the project')
        # self.parser.add_option('-d', '--directory', dest='base_directory',
        #                       help='Base directory the project is in')
        self.options, self.args = self.parser.parse_args()
        if self.options.rebuild:
            self._build_steps.insert(0, self.rebuild)
        if self.options.clean:
            self._build_steps.insert(0, self.clean)


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
