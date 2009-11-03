import os
import sys
import threading
from glob import glob
from datetime import datetime

from buildit.compiler.compiler import Compiler
from buildit.cprint import error, info
from buildit.utils import lookup_error, flatten
from buildit.utils import fix_strings
from buildit.utils import name as uname
from buildit.hashdb import HashDB

class System(threading.Thread):

    def __init__(self, project_name, unity_build=False):
        threading.Thread.__init__(self)
        self._compiler = Compiler()
        self._hashdb = HashDB(self.name)
        self._file_list = []
        self._build_steps = []
        self._unity_build = unity_build
        self._project_name = project_name
        self._build_directory = 'build/{0}'.format(self.name)
        self._object_directory = 'object/{0}'.format(self.name)
        self._unity_directory = 'unity/{0}'.format(self.name)

        self._build_steps.append(self.pre_build)
        self._build_steps.append(self.build)
        self._build_steps.append(self.post_build)

    def run(self):
        start_time = datetime.now()
        for function in self._build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}: {1}'.format(self.name.upper(), (end_time - start_time)))

    def pre_build(self):
        return 0
   
    def build(self):
        return_value = self._compiler.run(self._file_list, self._hashdb)
        return return_value

    def post_build(self):
        return 0

    def add_files(self, files):
        if isinstance(files, tuple) or isinstance(files, list):
            for item in flatten(files):
                if isinstance(item, basestring):
                    if os.path.isdir(item):
                        glob_list = glob('{0}/*'.format(item))
                        for file_name in glob_list:
                            self._file_list.append(file_name)
                    else:
                        self._file_list.append(item)
        elif isinstance(files, basestring):
            if os.path.isdir(files):
                glob_list = glob('{0}/*'.format(files))
                for item in glob_list:
                    self._file_list.append(item)
            else:
                self._file_list.append(files)
        else:
            warning('{0} is not a supported datatype!'.format(files))
    
    @property
    def compiler(self):
        return self._compiler

    @compiler.setter
    def compiler(self, value):
        self._compiler = value
        self._compiler.object_directory = self._object_directory
        self._compiler.build_directory = self._build_directory
        self._compiler.unity_directory = self._unity_directory

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
        ''' Set the System's object file directory '''
        self._object_directory = value
        self._compiler.object_directory = value
    
    @property
    def unity_directory(self):
        return self._unity_directory

    @unity_directory.setter
    def unity_directory(self, value):
        ''' Set the System's unity build directory '''
        self._unity_directory = value
        self._compiler.unity_directory = value
