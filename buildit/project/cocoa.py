# MAC OS X C/C++/ObjC Projects
from buildit.project.unix import Unix

class Cocoa(Unix):
    
    def __init__(self, project_name):
        Unix.__init__(self, project_name)
