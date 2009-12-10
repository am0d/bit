# Python "Compiler" Class
import os
import py_compile

from buildit.compiler.compiler import Compiler

from buildit.utils import format_options, fix_strings, file_hash
from buildit.cprint import command as print_command

class PYC(Compiler):
    
    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self._executable = 'pyc'

    def compile_files(self):
        counter = 1
        file_count = len(self._file_list)
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}c'.format(self.build_directory, file)
            if os.path.exists(out_file) and \
                hash == self.database.get_hash(file):
                file_count -= 1
                continue
            percentage = self._percentage(counter, file_count)
            object_directory = out_file.split('/')
            object_directory.pop()
            if len(object_directory) > 1:
                object_directory = '/'.join(object_directory)
            else:
                object_directory = object_directory.pop()
            info_file = file.split('/')
            info_file = info_file.pop()
            try:
                os.makedirs(object_directory)
            except OSError:
                pass
            self.command(percentage, info_file)
            try:
                py_compile.compile(file, out_file, doraise=True)
            except py_compile.PyCompileError:
                return 1002
            self.database.update_hash(file)
            counter += 1
        return 0

    @property
    def extensions(self):
        return ['.py']
