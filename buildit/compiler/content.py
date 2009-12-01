# Used for moving content to the build directory

import os
import shutil
import subprocess

from buildit.database import Database

from buildit.utils import flatten, fix_strings, file_hash
from buildit.utils import name as uname

class Content(Compiler):
    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)

    def compile_files(self):
        counter = 1
        file_count = len(self._file_list)
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}'.format(self.build_directory, file)
            if os.path.exists(out_file) and \
                hash == self.database.get_hash(file)
                continue
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
                shutil.copy2(file, out_file)
            except:
                error('Could not copy: {0}'.format(info_file))
            counter += 1
        return 0

    @property
    def extensions(self):
        return ['*'] # Allows the glob to automatically grab everything for content
