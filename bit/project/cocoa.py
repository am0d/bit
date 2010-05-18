# MAC OS X C/C++/ObjC Projects
from bit.project.unix import Unix
from bit.utils import flatten
class Cocoa(Unix):
    
    def __init__(self, project_name):
        Unix.__init__(self, project_name)

    def __str__(self):
        return 'Cocoa'

    def add_framework(self, *frameworks):
        for framework in flatten(list(set(frameworks))):
            self.compiler.add_compiler_flags('-framework', framework)
            self.compiler.add_linker_flags('-framework', framework)
