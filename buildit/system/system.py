import os
import sys
import threading

from buildit.compiler import compiler.Compiler as Compiler
from buildit.linker import linker.Linker as Linker

class System(threading.Thread):
    
    def __init__(self, unity_build=False):
        threading.Thread.__init__(self)
        self.compiler = Compiler()
        self.linker = Linker()
        self.file_list = []        
        self.build_steps = []
        self.unity_build = unity_build
        self.build_steps.append(pre_build)
        self.build_steps.append(build)
        self.build_steps.append(post_build)


    def run(self):
        for function in self.build_steps:
            return_value = function()
            if not return_value == 0:
                error('\nError: {0}'.format(lookup_error(return_value)))
                sys.exit(return_value)

    def pre_build(self):
        pass

    def build(self):
        self.compiler.run(self.unity_build)
        self.linker.run(self.unity_build)
        
    def post_build(self):
        pass

    def add_files(self, files):
        self.file_list.append(files) # Just temporary.
