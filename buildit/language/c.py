# Basic C Language Dependency Tracking

from buildit.language.generic import Generic

class C(Generic):

    def __init__(self):
        Generic.__init__(self)

    def get_file_deps(self, file_name):
        deps_list = []
        try:
            file = open(file_name, 'r')
            for line in file:
                dependency = self.parse_line(line)
                if not dependency == '':
                    deps_list.append(dependency)
            return deps_list
        except IOError:
            error('Unable to read dependencies for {0}'.format(file_name))
        finally:
            file.close()
