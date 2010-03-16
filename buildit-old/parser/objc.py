from buildit.parser.clanguage import CLanguage

class ObjC(CLanguage):
    
    def __init__(self):
        CLanguage.__init__(self)
        self.__keyword = '#import'
