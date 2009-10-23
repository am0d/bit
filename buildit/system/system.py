import os
import sys
import threading
import datetime.datetime as datetime

from buildit.compiler import compiler.Compiler as Compiler
from buildit.linker import linker.Linker as Linker
from buildit.cprint import error, info
from buildit.utils import fix_strings

class System(threading.Thread):
    
    def __init__(self, project_name,unity_build=False):
        threading.Thread.__init__(self)
        self.compiler = Compiler()
        self.linker = Linker()
        self.file_list = []        
        self.build_steps = []
        self.unity_build = unity_build
        self.project_name = project_name
        self.source_directory = 'source'
        self.build_directory = 'build'
        self.object_directory = 'object'
        
        self.build_steps.append(pre_build)
        self.build_steps.append(build)
        self.build_steps.append(post_build)


    def run(self):
        start_time = datetime.now()
        for function in self.build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)
        info('{0}: {1}'.format(self.name.upper(), datetime.now() - start_time))

    def pre_build(self):
        pass

    def build(self):
        self.compiler.run(self.unity_build)
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
        
    def source_directory(self, directory):
        ''' Set the System's base source directory '''
        self.source_directory = directory
        
    def build_directory(self, directory):
        ''' Set the System's build (output) directory'''
        self.build_directory = directory
        
    def object_directory(self, directory):
        ''' Set the System's object file directory '''
        self.object_directory = directory
