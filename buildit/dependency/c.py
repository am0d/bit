# C Language Dependency

from buildit.buildit.dependency import Dependency

class CDependency(Dependency):

    def __init__(self):
        self.extensions = ['h']
        self.keyword = '#include'

