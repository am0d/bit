# A very terrible hack, but some people probably won't want to do something
# like from buildit.compiler.compiler import Compiler. 
# This just saves them the trouble

# System Modules
from buildit.project import Project
from buildit.platform.unix import Unix

# Compiler Modules
from buildit.compiler.cc import CC
from buildit.compiler.cxx import CXX
from buildit.compiler.tcc import TCC
from buildit.compiler.llvmgcc import LLVMGCC

# Targets
from buildit.target.executable import Executable
from buildit.target.dynamiclibrary import DynamicLibrary
from buildit.target.staticlibrary import StaticLibrary
