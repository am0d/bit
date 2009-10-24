# Class Level functions (Used only on classes)

class_list = []

def add_project(project):
    if not isinstance(project, classobj):
        warning('{0} is not a recognized project type!'.format(project))
    class_list.append(project)
