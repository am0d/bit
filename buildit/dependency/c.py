# C Language Dependency

from buildit.utils import flatten
from buildit.buildit.dependency import Dependency

class CDependency(Dependency):

    def __init__(self):
        self.extensions = ['h']
        self.keyword = '#include'

    def parse(self, line):
        if self.keyword in line:
            return remove(line, '<', '>', '"', self.keyword).lstrip().rstrip()
        return ''

    def remove(string, *chars):
        for char in flatten(chars):
            string = string.replace(char, '')
        return string
