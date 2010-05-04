# GCC/G++ Projects

from buildit.project.project import Project
from buildit.compiler.gcc import GCC
from buildit.compiler.gpp import GPP
from buildit.linker.gcc import GCCLinker
from buildit.linker.gpp import GPPLinker

class GNUCC(Project):
    
    def __init__(self, project_name):
        Project.__init__(self)
        self.compiler_list = [GCC, GPP]
        self.linker = GCCLinker

    @property
    def enable_cpp(self):
        self.linker = GPPLinker

    @property
    def
