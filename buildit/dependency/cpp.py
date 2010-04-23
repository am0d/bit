# CPP Dependency

from buildit.buildit.c import CDependency

class CPPDependency(CDependency):

    def __init__(self):
        CDependency.__init__(self)
        self.extensions = ['h', 'hpp', 'hxx']
