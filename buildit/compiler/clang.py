# LLVM Clang Compiler

from buildit.compiler.cc import CC

class Clang(CC):
    
    def __init__(self):
        CC.__init__(self)
        self.executable = 'clang'

    def __str__(self):
        return 'CLANG'
