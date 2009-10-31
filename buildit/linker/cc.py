from builit.linker.linker import Linker
from buildit.utils import which

class CCLinker(Linker):

    @property
    def exe(self):
        which('cc')

    @property
    def extensions(self):
        return ['.o]
