# Imports our modules for local use, and creates our GPL instance

# Project Modules
from bit.project.cocoa import Cocoa
from bit.project.unix import Unix
from bit.project.mingw import MinGW
from bit.project.msvc import MSVC
from bit.project.content import Content

# Compiler Modules
from bit.compiler.cc import CC
from bit.compiler.clang import Clang
from bit.compiler.msvc import MSVCCompiler

# Global Project Lookup
from bit.gpl import GPL

# Magic
import sys

windows = False
macosx = False
linux = False
bsd = False

if sys.platform == 'win32':
    windows = True
if sys.platform == 'darwin':
    macosx = True
if sys.platform == 'linux2':
    linux = True
if 'bsd' in sys.platform:
    bsd = True
# Assuming Direct Control
bit = GPL()
