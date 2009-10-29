from buildit.linker.linker import Linker as Linker
from buildit.utils import which

class LD(Linker):

    def __init__(self):
        Linker.__init__(self)
        self.__source_option = ''
        self.__output_option = '-o'
    
    @property
    def exe(self):
        which('ld')

    @property
    def extensions(self):
        return ['.o']

    
