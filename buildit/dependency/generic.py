from buildit.dependency.dependency import Dependency

class Generic(Dependency):
    def parse_line(self, line, current_file):
        return ''
