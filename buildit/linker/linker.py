# Base Linker Class

class Linker(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.file_list = [ ]

    def run(self, file_list):
        self.file_list = file_list
