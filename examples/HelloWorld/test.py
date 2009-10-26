from buildit.system.system import System as System
from buildit.compiler.cc import CC as CC

linux = System("Hello World")
linux.add_files('source/hello.c')
linux.compiler = CC()
linux.run()
