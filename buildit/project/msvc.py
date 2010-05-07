# MSVC Project Class

from buildit.project.project import Project

class MSVC(Project):
    
    def __init__(self, project_name):
        Project.__init__(self, project_name)

    def __str__(self):
        return 'MSVC'
