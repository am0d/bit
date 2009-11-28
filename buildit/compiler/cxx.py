# Unix Based CXX Compiler

from buildit.compiler.cc import CC
from buildit.language.cpp import CPP
from buildit.utils import which

class CXX(CC):

    def __init__(self):
        CC.__init__(self)
        self._clang_enabled = False
        self.executable = 'c++'
        self._language = CPP()

    @property
    def extensions(self):
        if not self._clang_enabled:
            return ['.cpp', '.cxx', '.c++', '.C']
        else:
            return ['.c', '.cpp', '.cxx', '.c++', '.C']

    @property
    def module_extension(self):
        return ['.h', '.hpp', '.hxx', '.h++']

    @property 
    def enable_c(self):
        self._clang_enabled = True
