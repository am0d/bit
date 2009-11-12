# Base System Class

import os
import sys
import shutil
import threading
from glob import glob
from datetime import datetime

from buildit.compiler.compiler import Compiler
from buildit.filelist import FileList
from buildit.utils import lookup_error, flatten, fix_strings
from buildit.utils import name as uname
from buildit.cprint import error, info, warning

class System(threading.Thread):
    
    def __init__(self, project_name):
        threading.Thread.__init__(self)
        self._file_list = FileList(project_name)
        self._compiler = Compiler(self._file_list)
        self._build_steps = []
        self._project_name = project_name
        self._unity_directory = ''
        self._build_directory = ''
        self._object_directory = ''

        self.unity_directory = 'unity/{0}'.format(self.name)
        self.build_directory = 'build/{0}'.format(self.name)
        self.object_directory = 'object/{0}'.format(self.name)

        self._build_steps.append(self.pre_build)
        self._build_steps.append(self.build)
        self._build_steps.append(self.post_build)

        self.parse_commandline()

    def run(self):
        start_time = datetime.now()
        for function in self._build_steps:
            return_value = function()
            if not (return_value == 0 or return_value == None):
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}: {1}'.format(self._project_name.upper(),
                                (end_time - start_time)))

    def pre_build(self):
        return 0
    
    def build(self):
        return_value = self._compiler.run(self.name, 
            self._project_name)
        self._file_list.write_to_disk()

    def post_build(self):
        return 0

    def add(self, files):
        new_files = []
        if isinstance(files, (tuple, list)):
            for item in flatten(files):
                if isinstance(item, basestring):
                    if os.path.isdir(item):
                        glob_list = glob('{0}/*'.format(item))
                        for file_name in glob_list:
                            if os.path.isfile(file_name):
                                file_name = '{0}'.format(file_name)
                                new_files.append(file_name)
                    else:
                        item = '{0}'.format(item)
                        new_files.append(item)
        elif isinstance(files, (str, basestring)):
            if os.path.isdir(files):
                glob_list = glob('{0}/*'.format(files))
                for file_name in glob_list:
                    if os.path.isfile(file_name):
                        file_name = '{0}'.format(file_name)
                        new_files.append(file_name)
            else:
                item = '{0}'.format(item)
                new_files.append(files)
        else:
            warning('{0} is not a supported datatype.'.format(type(files)))
        new_files = fix_strings(new_files)
        self._file_list.add(new_files)
    
    def parse_commandline(self):
        for arg in sys.argv[1:]:
            if arg == '--generate-deps':
                self._build_steps.append(self.generate_dependencies)
            elif arg == '--rebuild':
                self._build_steps.insert(0, self.rebuild)
            elif arg == '--clean':
                self._build_steps = [self.clean]
            else:
                warning('Unknown argument {0}'.format(arg))

    def generate_dependencies(self):
        self._file_list.generate_dependencies()

    def clean(self):
        try:
            if os.path.exists(self._object_directory):
                shutil.rmtree(self._object_directory)
            if os.path.exists(self._build_directory):
                shutil.rmtree(self._build_directory)
            return 0
        except OSError:
            return 1005

    def rebuild(self):
        self.clean()
        return self._file_list.rebuild()

    @property
    def compiler(self):
        return self._compiler

    @compiler.setter
    def compiler(self, value):
        self._compiler = value
        self._compiler.object_directory = self._object_directory
        self._compiler.build_directory = self._build_directory
        self._compiler.unity_directory = self._unity_directory
        self._compiler.file_list = self._file_list

    @property
    def name(self):
        return uname(self)

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
        self._file_list.set_object_directory(value)

    @property
    def unity_directory(self):
        return self._unity_directory

    @unity_directory.setter
    def unity_directory(self, value):
        self._unity_directory = value

    @unity_directory.setter
    def unity_directory(self, value):
        self._unity_directory = value
        self._compiler.unity_directory = value
