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
        msvc_path = fix_strings(msvc_path)
        msvc_path = msvc_path.split('/')
        msvc_path.pop(), msvc_path.pop(), msvc_path.pop()
        self.add_path('{0}/VC/Bin'.format(msvc_path))
        self.add_path('{0}/Common7/ID'.format(msvc_path))
        path_list = []
        for path in os.environ['LIB'].split(os.pathsep):
            path_list.append(path)
        lib_string = '/amd64' if self.__arch == 64 else ''
        path_list.append('{0}/VC/lib{1}'.format(msvc_path, lib_string))
        path_list = os.pathsep.join(path_list)
        os.environ['LIB'] = path_list
        path_list = []
        for path in os.environ['INCLUDE'].split(os.pathsep):
            path_list.append(path)
        path_list.append('{0}/VC/include'.format(msvc_path))
        path_list.append('{0}/VC/atlmfc/include'.format(msvc_path))
        path_list = os.pathsep.join(path_list)
        os.environ['INCLUDE'] = path_list

    def add_define(self, *defines): 
        self.compiler.add_define(*defines)

    def add_library(self, *libraries):
        self.compiler.add_library(*libraries)

    def add_library_directory(self, *directories):
        self.compiler.add_library_directory(*directories)

    def add_include_directory(self, *directories):
        self.compiler.add_include_directory(*directories)

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
        self.__compiler_version = 'VS100COMNTOOLS'