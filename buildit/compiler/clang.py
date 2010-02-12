# LLVM Clang Compiler
# As soon as C++ support is stable, this be change wildly 
# to differentiate from CC
from buildit.compiler.cc import CC

class Clang(CC):
    
    def __init__(self):
        CC.__init__(self)
        self.executable = 'clang'

    def __str__(self):
        return 'CLANG'
