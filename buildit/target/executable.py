from buildit.target.target import Target

class Executable(Target):
    def __init__(self, name='Executable'):
        Target.__init__(self, name)

    def printout(self):
        print "Hello"

