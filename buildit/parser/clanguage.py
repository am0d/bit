from buildit.parser.parser import Parser
from buildit.utils import flatten
from buildit.cprint import error

class CLanguage(Parser):
    
    def __init__(self):
        Parser.__init__(self)
        self._keyword = '#include'

    def parse(self, file_name):
        deps_string = []
        with open(file_name) as file:
            for line in file:
                if self._keyword in line:
                    self._line_list.append(line)
        for line in self._line_list:
            line = line.replace(self._keyword,'')
            line = line.replace(' ', '')
            if '"' in line:
                line = line.split('"').pop()
            elif '<' in line:
                line = line.replace('<', '')
                line = line.split('>').pop()
            else:
                error('False positive detected in {0}'.format(file_name))
            deps_string.append(line)
        
