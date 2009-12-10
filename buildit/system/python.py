# Python System Class

from buildit.system.system import System
from buildit.compiler.pyc import PYC

class Python(System):
    def __init__(self, project_name):
        System.__init__(self, project_name)
        self.compiler = PYC()
