# Used for files, and other non compiled stuff

from buildit.system.system import System 
from buildit.compiler.content import Content as ContentC

class Content(System):

    def __init__(self):
        System.__init__(self, 'Content')
        self.compiler = ContentC()

    def __str__(self):
        return 'Content'
