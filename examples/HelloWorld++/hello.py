from buildit import Unix
from buildit import CXX


hello = Unix('Hello World')
hello.add('src')
hello.compiler = CXX()
hello.run()
