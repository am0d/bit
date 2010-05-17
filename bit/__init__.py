# Imports our modules for local use, and creates our GPL instance

# Project Modules
from bit.project.cocoa import Cocoa
from bit.project.msvc import MSVC
from bit.project.unix import UNIX

# Compiler Modules
from bit.compiler.gcc import GCC

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
