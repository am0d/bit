# Base Compiler Class

from buildit.utils import which

class Compiler(object):

    def __init__(self):
        self.file_list = []
        self.exe = which('echo')
        self.extensions = ['.txt']

    def run(self):
        pass

    
