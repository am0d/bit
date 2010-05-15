# Imports our modules for local use, and creates our GPL instance

# Project Modules
from buildit.project.cocoa import Cocoa
from buildit.project.msvc import MSVC
from buildit.project.unix import UNIX

# Compiler Modules
from buildit.compiler.gcc import GCC
from buildit.compiler.gpp import GPP

# Global Project Lookup
from buildit.gpl import GPL

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
buildit = GPL()
