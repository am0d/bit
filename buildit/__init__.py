# Imports out modules locally, and creates our GPL instance :)

# System Modules
from buildit.system.system import System
from buildit.system.unix import Unix
from buildit.system.mingw import MinGW
from buildit.system.content import Content

# Compiler Modules
from buildit.compiler.cc import CC
from buildit.compiler.tcc import TCC
from buildit.compiler.llvmgcc import LLVMGCC
from buildit.compiler.clang import Clang
from buildit.compiler.msvc import MSVC

# Global Project Lookup
from buildit.gpl import GPL

buildit = GPL()
