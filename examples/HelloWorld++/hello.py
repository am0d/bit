from buildit.system.unix import Unix
from buildit.compiler.cxx import CXX

hello = Unix('Hello World')
hello.add('src')
hello.compiler = CXX()
hello.run()
