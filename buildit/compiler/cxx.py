# Unix Based CXX Compiler

from buildit.compiler.cc import CC
from buildit.utils import which

class CXX(CC):

    def __init__(self):
        CC.__init__(self)
        self._executable = which('c++')
        self._language = 'CPP'

    @property
    def extensions(self):
        return ['.cpp', '.cxx', '.c++', '.C']

    @property
    def never_compile(self):
        return ['.h', '.hpp']
