# Unix Based CXX Compiler

from buildit.compiler.cc import CC
from buildit.utils import which

class CXX(CC):

    def __init__(self):
        CC.__init__(self)
        self._clang_enabled = False
        self.executable = 'c++'

    def __str__(self):
        return 'CXX'

    @property
    def extensions(self):
        if not self._clang_enabled:
            return ['.cpp', '.cc', '.cxx', '.c++', '.C'] + self.user_extensions
        else:
            return ['.c', '.cc', '.cpp', '.cxx', '.c++', '.C']

    @property
    def dependency_extension(self):
        return ['.h', '.hpp', '.hxx', '.h++'] + self.user_dependencies

    @property 
    def enable_c(self):
        self._clang_enabled = True
