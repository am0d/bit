# Tiny C Compiler

from buildit.compiler.cc import CC

class TCC(CC):

    def __init__(self):
        CC.__init__(self)
        self.executable = 'tcc'

    def __str__(self):
        return 'TCC"
