# Basic Unix Program

from buildit.project.project import Project
from buildit.compiler.gcc import GCC
class Unix(Project):

    def __init__(self, project_name):
        Project.__init__(self, project_name)
        self.compiler = GCC(self.project_name)

    def __str__(self):
        return 'Unix'
