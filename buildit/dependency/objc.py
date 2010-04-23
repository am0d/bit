# Objective-C Dependency

from buildit.dependency.c import CDependency

class ObjCDependency(CDependency):

    def __init__(self):
        CDependency.__init__(self)
        self.keyword = '#import'
