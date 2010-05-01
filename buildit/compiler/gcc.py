import os
import sys
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.utils import flatten

class GCC(Compiler):

    def __init__(self, project_name, file_list):
        self.file_extensions = ['c', 'm']
        self.executable = 'gcc'
        self.output_extension = 'o'

    def __str__(self):
        return 'gcc'

    def compile_files(self):
        counter = 1
        job_list = [ ]
        for file_name in self.file_list:
            out_file = '{0}/{1}.{2}'.format(self.output_directory, file_name, self.output_extension)
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
            # We have no way to determine if the directories already exist
            # or if there was a catastrophe. But we'll find out soon enough. :D
            except OSError:
                pass
        
            if self.type == 'dynamic'
                self.add_compiler_flags('-fPIC')
            # TODO: Change to using a list, which allows subprocess.call to not kill itself
            run_string = '{0} -o "{1}" -c "{2}" {3}'.format(self.executable, out_file, file_name, 
                     ' '.join(self.compile_flags))
            try: 
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            self.completed_files.append(out_file)
            counter += 1
        return 0
