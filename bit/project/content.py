# Used for copying data

from bit.project.project import Project
from buildit.compiler.content import Content as ContentCompiler

class Content(Project):

    def __init__(self):
        Project.__init__(self, 'Content')
        self.compiler = ContentCompiler()

    def __str__(self):
        return 'Content'
