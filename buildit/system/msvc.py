# Microsoft Visual C Compiler

from buildit.system.unix import Unix
from buildit.utils import which
from buildit.cprint import error

class MSVC(System)

    def __init__(self, project_name):
        self.compiler.executable = 'cl'
