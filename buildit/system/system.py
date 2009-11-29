# Base System Class

import os
import gc
import sys
import shutil
import threading
from glob import glob
from datetime import datetime

from buildit.compiler.compiler import Compiler
from buildit.database import Database
from buildit.utils import lookup_error, flatten, fix_strings
from buildit.utils import name as uname
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

    def build(self):
        return_value = self.compiler.run
        return return_value

    def append(self, function):
        self._build_steps.append(function)

    def prepend(self, function):
        self._build_steps.insert(function, 0)

    def pause(self):
        raw_input('Press Enter to continue...')

    def add(self, files, recurse=False):
        if isinstance(files, (tuple,list)):
            for item in flatten(files):
                if isinstance(item, basestring):
                    if os.path.isdir(item):
                        glob_list = []
                        if recurse:
                            for root, dir, files in os.walk(item):
                                glob_list += glob('{0}/*'.format(root))
                        else:
                            glob_list = glob('{0}/*'.format(item))
                        for file_name in glob_list:
                            if os.path.isfile(file_name):
                                self._file_list.append(file_name)
                    else:
                        self._file_list.append(item)
        elif isinstance(files, basestring):
            if os.path.isdir(files):
                glob_list = []
                if recurse:
                    for root, dir, file_names in os.walk(files):
                        glob_list += glob('{0}/*'.format(root))
                else:
                    glob_list = glob('{0}/*'.format(files))
                for file_name in glob_list:
                    if os.path.isfile(file_name):
                        self._file_list.append(file_name)
            else:
                self._file_list.append(files)
        else:
            warning('{0} is not a supported datatype'.format(type(files)))
        if sys.platform == 'win32':
            self._file_list = fix_strings(self._file_list)
        self._file_list.sort()
        self.compiler._file_list = self._file_list

    def remove(self, files):
        if isinstance(files, (tuple, list)):
            for item in flatten(files):
                if isinstance(item, basestring):
                    if os.path.isdir(item):
                        glob_list = glob('{0}/*'.format(item))
                        for file_name in glob_list:
                            if os.path.isfile(file_name):
                                try:
                                    self._file_list.remove(file_name)
                                except ValueError:
                                    warning('{0} could not be removed'.format(
                                        file_name))
                    else:
                        try:
                            self._file_list.remove(file_name)
                        except ValueError:
                            warning('{0} could not be removed'.format(
                                file_name))
        elif isinstance(files, basestring):
            if os.path.isdir(files):
                glob_list = glob('{0}/*'.format(files))
                for file_name in glob_list:
                    if os.path.isfile(file_name):
                        try:
                            self._file_list.remove(file_name)
                        except ValueError:
                            warning('{0} could not be removed'.format(
                                file_name))
            else:
                try:
                    self._file_list.remove(file_name)
                except ValueError:
                    warning('{0} could not be removed'.format(file_name))
        else:
            warning('{0} is not a supported datatype.'.format(type(files)))
        self._file_list.sort()
        self.compiler._file_list = self._file_list

    def require(self, required_system):
        self._build_steps.insert(0, required_system.run())

    def clean(self):
        try:
            if os.path.exists(self.build_directory):
                shutil.rmtree(self.build_directory)
            if os.path.exists(self.object_directory):
                shutil.rmtree(self.object_directory)
        except OSError:
            error('Failed to clean {0}'.format(self._project_name))
            return 1005
        return 0
        
    def parse_options(self):
        for arg in sys.argv[1:]:
            if arg == '--clean':
                self._build_steps = [self.clean]
            elif arg == '--rebuild':
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
        return uname(self)

    @property
    def compiler(self):
        return self._compiler

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
