# Basic C Language Dependency Tracking

from buildit.dependency.dependency import Dependency

class C(Dependency):

    def __init__(self, name, directories=[]):
        Dependency.__init__(self, name, directories)
        self.header = 'CLANG'
        self._magic_word = '#include'
