# GCC Compiler
import os
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.cprint import command

class GCC(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)
        self.compiler = 'gcc'
        self.linker = 'gcc'
        self.output_extension = 'o'

    def __str__(self):
        return 'gcc'

    def compile_files(self):
        counter = 1
        for file_name in self.file_list:
            out_file = '{0}/{1}.{2}'.format(self.object_directory, file_name, self.output_extension)
            percentage = self.percentage(counter, self.file_count)
            object_directory = out_file.split('/')
            object_directory.pop()
            if len(object_directory) > 1:
                object_directory = '/'.join(object_directory)
            else:
                object_directory = object_directory.pop()
            info_file = file_name.split('/').pop()
            try:
                os.makedirs(object_directory)
            # With no way with which to discern why makedirs fails, we must unfortunately pass
            except OSError:
                pass
            if self.type == 'dynamic':
                self.add_compiler_flags('-fPIC')
            run_list = [self.compiler, '-o' '"{0}"'.format(out_file), '-c', 
                        '"{0}"'.format(file_name)] + self.compiler_flags
            try:
                return_value = subprocess.call(run_list)
            except OSError:
                return_value = os.system(' '.join(run_list))
            if not return_value == 0:
                return return_value
            counter += 1
        return 0

    def link_files(self):
        try:
            os.makedirs(self.output_directory)
        except OSError:
            pass
        run_list = [self.linker, '-o', '"{0}"'] + self.link_list + self.linker_flags
        command('[LINK] {0}'.format(self.project_name))
        try:
            subprocess.call(run_list)
        except OSError:
            os.system(' '.join(run_list))
        return 0

    @property
    def C99(self):
        pass

    @property
    def CXX(self):
        pass

    @property
    def enable_c(self):
        pass
