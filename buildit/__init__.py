# A very terrible hack, but some people probably won't want to do something
# like from buildit.compiler.compiler import Compiler. 
# This just saves them the trouble

# Dependency Modules
from buildit.dependency.c import C
from buildit.dependency.cpp import CPP

# Compiler Modules
from buildit.compiler.cc import CC
from buildit.compiler.cxx import CC
from buildit.compiler.tcc import TCC
from buildit.compiler.llvmgcc import LLVMGCC
