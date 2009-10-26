# Unix Based C Compiler

from buildit.compiler.compiler import Compiler as Compiler

from buildit.utils import which

class CC(Compiler):
    
    @property
    def exe(self):
        return which('cc')
    
    @property    
    def extensions(self):
        return ['.c']

    @property
    def output_extension(self):
        return '.o'
        
    def add_includes(self, directory):
        self.flags += format_options(directory, '-I')
    
    def add_define(self, define):
        self.flags += format_options(define, '-D')
