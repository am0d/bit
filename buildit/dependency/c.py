# C Language Dependency

import re

from buildit.buildit.dependency import Dependency

class CDependency(Dependency):

    def __init__(self):
        self.extensions = ['h']
        self.word = 'include'
        self.exp = ''.join(['.*?({0}).*?((?:[a-z][a-z]+))'.format(self.word),
                            '.*?((?:[a-z][a-z0-9_]*))'])
        self.regex = re.compile(self.exp, re.IGNORECASE)
