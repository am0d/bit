# Windows Based C/C++ System (GCC BASED)

from buildit.system.unix import Unix

class MinGW(Unix):

    def __init__(self, project_name):
        Unix.__init__(self, project_name)
        self.compiler.executable = 'gcc' 
