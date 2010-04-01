# Imports our modules for local use, and creates our GPL instance

# System Modules

# Compiler Modules

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
