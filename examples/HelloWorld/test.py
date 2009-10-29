from buildit.system.system import System as System
from buildit.compiler.cc import CC as CC
from buildit.linker.ld import LD as LD

linux = System("Hello World")
linux.add_files('source/hello.c')
linux.compiler = CC()
linux.linker = LD()
linux.linker.target = 'HelloWorld'
linux.run()
