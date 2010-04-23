# Base Dependency Class

class Dependency(object):

    def __init__(self):
        self.extensions = ['txt'] 
        self.keyword = 'generic'
    
    # Returns a list of files
    def find(self, file_name):
        with open(file_name) as file:
            return [parse(line) for line in file]

    # Override this.
    def parse(self, line):
        if self.keyword in line:
            return line
