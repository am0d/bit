from buildit import *

hello = Unix('Hello World')
hello.add('src')
hello.compiler = CXX()
hello.run()
