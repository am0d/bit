# Imports out modules locally, and creates our GPL instance, and 
# sets up a few other things as well :)

# System Modules
from buildit.platform.platform import Platform
from buildit.platform.unix import Unix
from buildit.platform.mingw import MinGW
from buildit.platform.content import Content

# Compiler Modules
from buildit.compiler.cc import CC
from buildit.compiler.tcc import TCC
from buildit.compiler.llvmgcc import LLVMGCC
from buildit.compiler.clang import Clang
from buildit.compiler.msvc import MSVC

# Global Project Lookup
from buildit.gpl import GPL

# Magic?
import sys

windows = False
macosx = False
linux = False

if sys.platform == 'win32':
    windows = True
if sys.platform == 'darwin':
    macosx = True
if sys.platform == 'linux2':
    linux = True

# Assuming Direct Control
buildit = GPL()
