import os
import sys
import threading
from datetime import datetime as datetime

from buildit.compiler.compiler import Compiler as Compiler
from buildit.linker.linker import Linker as Linker
from buildit.cprint import error, info
from buildit.utils import lookup_error
from buildit.utils import fix_strings
from buildit.utils import name
from buildit.hashdb import HashDB

class System(threading.Thread):

    def __init__(self, project_name, unity_build=False, linker=True):
        threading.Thread.__init__(self)
        self.compiler = Compiler()
        self.linker = Linker()
        self.__hashdb = HashDB(self.name)
        self.__file_list = []        
        self.__build_steps = []
        self.__unity_build = unity_build
        self.__project_name = project_name
        self.__source_directory = 'source'
        self.__build_directory = 'build'
        self.__object_directory = 'object'
        self.__unity_directory = 'unity'

        self.__build_steps.append(self.pre_build)
        self.__build_steps.append(self.build)
        self.__build_steps.append(self.post_build)

    def run(self):
        start_time = datetime.now()
        for function in self.__build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}: {1}'.format(self.name.upper(), (end_time - start_time)))

    def pre_build(self):
        return 0

    def build(self):
        return_value = self.compiler.run(self.__file_list, self.__unity_build)
        if not return_value == 0:
            return return_value
        if self.linker == True:
            return_value = self.linker.run(self.__unity_build)
        return return_value
 
    def post_build(self):
        return 0

    def add_files(self, files):
        if isinstance(files, tuple) or isinstance(files, list):
            for item in flatten(files):
                if isinstance(item, basestring):
                    self.__file_list.append(item)
        elif isinstance(files, basestring):
            self.__file_list.append(files)
        else:
            warning('{0} is not a supported datatype!'.format(files))

    @property
    def name(self):
        return name(self)
        
    @property
    def source_directory(self):
        pass
        
    @source_directory.setter
    def source_directory(self, value):
        ''' Set the System's base source directory '''
        self.__source_directory = value

    @property
    def build_directory(self):
        pass

    @build_directory.setter
    def build_directory(self, value):
        ''' Set the System's build (output) directory '''
        self.__build_directory = value

    @property
    def object_directory(self):
        pass
    
    @object_directory.setter    
    def object_directory(self, value):
        ''' Set the System's object file directory '''
        self.__object_directory = value
    
    @property
    def unity_directory(self):
        #return self.__unity_directory
        pass

    @unity_directory.setter
    def unity_directory(self, value):
        ''' Set the System's unity build directory '''
        self.__unity_directory = value
