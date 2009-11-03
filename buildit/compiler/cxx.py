# Unix Based CXX Compiler

from buildit.compiler.cc import CC
from buildit.utils import which

class CXX(CC):

    def __init__(self):
        CC.__init__(self)
        self._executable = which('c++')

    @property
    def extensions(self):
        return ['.cpp', '.cxx', '.c++', '.C']
