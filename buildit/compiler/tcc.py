# Tiny C Compiler

from buildit.compiler.cc import CC
from buildit.utils import which

class TCC(CC):

    def __init__(self):
        CC.__init__(self)
        self._executable = which('tcc')
