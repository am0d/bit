# LLVM GCC Compiler

from buildit.compiler.cc import CC

class LLVMGCC(CC):

    def __init__(self):
        CC.__init__(self)
        self.executable = 'llvm-gcc'

    def __str__(self):
        return 'LLVM'
