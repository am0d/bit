# Base Dependency Class

import re

class Dependency(object):

    def __init__(self):
        self.extensions = ['txt']
        self.word = 'generic'
        self.exp = ''.join(['{0}'.format(self.word)])
        self.regex = re.compile(self.exp, re.IGNORECASE)

    # Returns a list of files
    def find(self, file_name):
        # Doesn't do anything yet :X
        temp = self.regex.search('')
        x = temp.group(0)
        return [ ]
