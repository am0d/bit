# Clang Compiler

from bit.compiler.cc import CC

class Clang(CC):
    
    def __init__(self, project_name):
        CC.__init__(self, project_name)
        self.executable = 'clang'
        
    def __str__(self):
        return 'Clang'

    @property
    def CXX(self):
        self.executable = 'clang++'
        self.cxx_support = True
