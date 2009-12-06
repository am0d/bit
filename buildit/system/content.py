# Used for files, and other non compiled stuff

from buildit.system.system import System 
from buildit.compiler.content import Content as ContentC

class Content(System):

    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = ContentC(project_name)
