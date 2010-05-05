# GCC Compiler
import os
import subprocess

from buildit.compiler.compiler import Compiler

class GCC(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self)
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
            run_list = [self.executable = '-o' '"{0}"'.format(out_file), '-c', 
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
        return 0
