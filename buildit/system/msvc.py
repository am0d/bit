# Microsoft Visual C Compiler

from buildit.system.system import System
from buildit.compiler.msvc import MSVC as MSVCompiler
from buildit.utils import which
from buildit.cprint import error

class MSVC(System):

    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = MSVCompiler()
        self.__compiler_version = 2008 # Used only to help figure out the install path
        self.__arch = 32 # Everyone uses 32 bit right? RIGHT?
        self._build_steps.insert(setup_environment, 0)

    # Sets up our system path for MSVC (so others don't have to)
    def setup_environment(self):
        return 0

    @property
    def x64(self):
        self.__arch = 64

    @property
    def vs6(self): #Are you crazy?!
        self.__compiler_version = 6

    @property
    def vs2003(self):
        self.__compiler_version = 2003

    @property
    def vs2005(self):
        self.__compiler_version = 2005

    @property
    def vs2008(self):
        self.__compiler_version = 2008

    @property
    def vs2010(self):
        self.__compiler_version = 2010
