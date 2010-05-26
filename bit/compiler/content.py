import os
import shutil
import filecmp
import subprocess

from bit.compiler.compiler import Compiler
from bit.utils import flatten

class Content(Compiler):

    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self.compiler = 'echo'

    def __str__(self):
        return 'Content Copier'

    def setup_files(self):
        self.file_list = flatten(list(set(self.file_list)))
        final_list = [ ]
        for file_name in self.file_list:
            out_file = '{0}/{1}'.format(self.build_directory, file_name)
            try:
                if not filecmp.cmp(file_name, out_file):
                    final_list.append(file_name)
            except OSError:
                pass
        self.file_list = proper_list
        self.file_count = len(self.file_list)

    def compile_files(self):
        counter = 1
        for file_name in self.file_list:
            percentage = self.percentage(counter, self.file_count)
            out_file = '{0}/{1}'.format(self.build_directory, file_name)
            info_file = file_name.split('/').pop()
            build_directory = out_file.split('/')
            build_directory.pop()
            try:
                os.makedirs(build_directory)
            except OSError:
                pass
            self.format_command(percentage, info_file)
            try:
                shutil.copy2(file, out_file)
            except OSError:
                error('Could not copy: {0}'.format(file_name))
            counter += 1
        return 0
