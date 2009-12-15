# Used for moving content to the build directory

import os
import shutil
import filecmp
import subprocess

from buildit.compiler.compiler import Compiler

from buildit.utils import flatten, fix_strings, file_hash
from buildit.utils import name as uname

class Content(Compiler):
    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self.executable = 'echo'

    def compile_files(self):
        counter = 1
        file_count = len(self._file_list)
        for file in self._file_list:
            check_file = file
            hash = file_hash(file)
            file = file.split('/')
            content = file.pop(0)
            if len(file) > 1:
                file = '/'.join(file)
            else:
                file = file.pop()
            out_file = '{0}/{1}'.format(self.build_directory, file)
            try:
                if filecmp.cmp(check_file, out_file):
                    continue
            except OSError:
                pass
            percentage = self._percentage(counter, file_count)
            build_directory = out_file.split('/')
            build_directory.pop()
            if len(build_directory) > 1:
                build_directory = '/'.join(build_directory)
            else:
                build_directory = build_directory.pop()
            info_file = file.split('/')
            info_file = info_file.pop()
            try:
                os.makedirs(build_directory)
            except OSError:
                pass
            self.command(percentage, info_file)
            try:
                file = '{0}/{1}'.format(content, file)
                shutil.copy2(file, out_file)
            except:
                error('Could not copy: {0}'.format(info_file))
            counter += 1
        return 0

    @property
    def extensions(self):
        return ['.*'] # Allows the glob to automatically grab everything for content
