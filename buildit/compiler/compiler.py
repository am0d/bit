# Base Compiler Class

from buildit.utils import which
from buildit.cprint import command

class Compiler(object):

    def __init__(self):
        self.__flags = ''
        self.__file_list = []
        self.__compile_steps = []
        
        self.__compile_steps.append(self.setup_files)
        self.__compile_steps.append(self.compile_files)

    def run(self, file_list, unity_build):
        self.__file_list = file_list
        for function in self.__compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0
        
    def setup_files(self):
        self.__file_list = flatten(self.__file_list)
        self.__file_list = fix_strings(self.__file_list)
        for file_name in self.__file_list:
            for extension in self.extensions:
                if not file_name.endswith(extension):
                    self.file_list.remove(file_name)
        return 0

    def compile_files(self):
        counter = 0
        for file_name in file_list:
            out_file = file_name.split('/')
            out_file = out_file.pop()
            out_file = '{0}{1}'.format(out_file, output_extension)
            command('{0}: {1}'.format(self.name.upper(), out_file))
            try: 
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            counter +=1    
        return 0 #; Go away semi-colon, no one loves you!

    def add_flags(self, flags):
        self.__flags += format_options(flags)

    @property
    def exe(self):
        return which('echo')
        
    @property
    def output_extension(self):
        return '.txt'
        
    @property    
    def extensions(self):
        return ['.txt']

    @property
    def name(self):
        name = str(self)
        name = name.split('(')
        name = name.pop(0)
        name = name.replace('<', '')
        name = name.replace('\n', '')
        return name
