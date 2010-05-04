# G++ Linker

from buildit.linker.gcc import GCCLinker

class GPPLinker(GCCLinker):
    
    def __init__(self, project_name):
        GCCLinker.__init__(self)
        self.executable = 'g++'
