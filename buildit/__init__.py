# A very terrible hack, but some people probably won't want to do something
# like from buildit.compiler.compiler import Compiler. 
# This just saves them the trouble

# System Modules
from buildit.system.system import System
from buildit.system.unix import Unix
from buildit.system.mingw import MinGW
from buildit.system.content import Content

# Compiler Modules
from buildit.compiler.content import Content
from buildit.compiler.cc import CC
from buildit.compiler.cxx import CXX
from buildit.compiler.tcc import TCC
from buildit.compiler.llvmgcc import LLVMGCC
