# C++ Language Dependency

from buildit.dependency.c import C

class CPP(C):

    def __init__(self, name, directories=[]):
        C.__init__(self, name, directories)
        self.header = 'CPP'
        self._magic_word = '#include'
