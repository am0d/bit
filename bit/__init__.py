# Imports our modules for local use, and creates our GPL instance

# Project Modules
from bit.project.cocoa import Cocoa
from bit.project.unix import Unix
from bit.project.mingw import MinGW
from bit.project.msvc import MSVC
from bit.project.content import Content

# Compiler Modules
from bit.compiler.cc import CC

# Global Project Lookup
from bit.gpl import GPL

# Magic
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
bit = GPL()