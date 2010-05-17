# MSVC Project Class

from bit.project.project import Project

class MSVC(Project):
    
    def __init__(self, project_name):
        Project.__init__(self, project_name)

    def __str__(self):
        return 'MSVC'
