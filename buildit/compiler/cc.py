# Unix Based C Compiler

from buildit.compiler import compiler.Compiler as Compiler

class CC(Compiler):
    
    def exe(self):
        return which('cc')
        
    def extensions(self):
        return ['.c']
        
    def add_includes(self, directory):
        self.flags += format_options(directory, '-I')
    
    def add_define(self, define):
        self.flags += format_options(define, '-D')