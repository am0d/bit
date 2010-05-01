# G++ Compiler

from buildit.compiler.gcc import GCC

class GPP(GCC):

    def __init__(self, project_name, file_list):
        GCC.__init__(self)
        self.file_extensions = ['.cpp', '.cc', '.cxx', '.mm']
        self.executable = 'g++'

    def __str__(self):
        return 'g++'
