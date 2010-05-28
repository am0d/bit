# MAC OS X C/C++/ObjC Projects
from bit.project.unix import Unix
from bit.utils import flatten
class Cocoa(Unix):
    
    def __init__(self, project_name):
        Unix.__init__(self, project_name)

    def __str__(self):
        return 'Cocoa'

    def framework(self, *frameworks):
        for framework in flatten(list(set(frameworks))):
            self.compiler.lflags('-framework', framework)

    def arch(self, *arches):
        for arch in flatten(list(set(arches))):
            self.compiler.cflags('-arch', arch)
            self.compiler.lflags('-arch', arch)
