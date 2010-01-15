# Microsoft Visual C Compiler

from buildit.system.system import System
from buildit.compiler.msvc import MSVC as MSVCompiler
from buildit.utils import which, fix_strings
from buildit.cprint import error

class MSVC(System):

    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = MSVCompiler()
        self.__compiler_version = 'VS90COMNTOOLS' # Used only to help figure out the install path
        self.__arch = 32 # Everyone uses 32 bit right? RIGHT?
        self.__setup_environment() # It should not be part of the build steps.

    def __str__(self):
        return 'MSVC'

    # Sets up our system path for MSVC (so others don't have to)
    def __setup_environment(self):
        msvc_path = [os.environ[self.__compiler_version]]
        self.add_path(fix_strings(msvc_path).pop())
        path_list = []
        for path in os.environ['LIB']:
            path_list.append(path)
        path_list.append(temp_string)
        path_list = os.pathsep.join(path_list)
        os.environ['LIB'] = path_list

    def add_define(self, define): pass

    def add_library(self, library, global_var=False): pass

    def add_library_directory(self, directory, global_var=False): pass

    def add_include_directory(self, directory, global_var=False): pass

    @property
    def x64(self):
        self.__arch = 64

    @property
    def vs6(self): #Are you crazy?!
        self.__compiler_version = 'VS90COMNTOOLS' # Doesn't work yet!

    @property
    def vs2003(self):
        self.__compiler_version = 'VS71COMNTOOLS'

    @property
    def vs2005(self):
        self.__compiler_version = 'VS80COMNTOOLS'

    @property
    def vs2008(self):
        self.__compiler_version = 'VS90COMNTOOLS'

    @property
    def vs2010(self):
        self.__compiler_version = 'VS100COMNTOOLS' # Not considered accurate right now XD
