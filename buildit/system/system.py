import os
import sys
import threading
from datetime import datetime as datetime

from buildit.compiler.compiler import Compiler as Compiler
#from buildit.linker.linker import Linker as Linker
from buildit.cprint import error, info
from buildit.utils import fix_strings

class System(threading.Thread):
    
    def __init__(self, project_name, unity_build=False, linker=True):
        threading.Thread.__init__(self)
        self.compiler = Compiler()
        #self.linker = Linker()
        self.file_list = []        
        self.build_steps = []
        self.unity_build = unity_build
        self.project_name = project_name
        self.source_directory = 'source'
        self.build_directory = 'build'
        self.object_directory = 'object'
        self.unity_directory = 'unity'
        
        self.build_steps.append(self.pre_build)
        self.build_steps.append(self.build)
        self.build_steps.append(self.post_build)


    def run(self):
        start_time = datetime.now()
        for function in self.build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        end_time = datetime.now()
        info('{0}: {1}'.format(self.name.upper(), (end_time - start_time)))

    def pre_build(self):
        pass

    def build(self):
        self.compiler.run(self.unity_build)
        if self.linker == True:
            self.linker.run(self.unity_build)
        
    def post_build(self):
        pass

    def name(self):
        name = str(self)
        name = name.split('(')
        name = name.pop(0)
        name = name.replace('<', '')
        name = name.replace('\n', '')
        return name

    def add_files(self, files):
        self.file_list.append(files) # Just temporary~
        
    @property
    def source_directory(self):
        pass
        
    @source_directory.setter
    def source_directory(self, value):
        ''' Set the System's base source directory '''
        self.source_directory = value

    @property
    def build_directory(self):
        pass

    @build_directory.setter
    def build_directory(self, value):
        ''' Set the System's build (output) directory '''
        self.build_directory = value

    @property
    def object_directory(self):
        pass
    
    @object_directory.setter    
    def object_directory(self, value):
        ''' Set the System's object file directory '''
        self.object_directory = value
    
    @property
    def unity_directory(self):
        pass

    @unity_directory.setter
    def unity_directory(self, value):
        ''' Set the System's unity build directory '''
        self.unity_directory = value
