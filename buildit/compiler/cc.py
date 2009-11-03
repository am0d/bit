# Unix Based C Compiler

import os
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.utils import which
from buildit.cprint import command

class CC(Compiler):

    def __init__(self):
        Compiler.__init__(self)
        self._executable = which('cc')
    
    def compile_files(self):
        counter = 1
        for file in self._file_list:
            module = ''
            percentage = self._percentage(counter, len(self._file_list))
            file_name = file.split('/')
            subdir = file_name
            file_name = file_name.pop()
            if len(subdir) > 1:
                subdir = '/'.join(subdir)
            else:
                subdir = subdir.pop()
            out_file = '{0}/{1}.o'.format(self._object_directory, file)
            try:
                os.makedirs('{0}/{1}'.format(self._object_directory, subdir))
            except OSError:
                pass
            self._info_string(percentage, file_name)
            run_string = '{0} -o {1} -c {2} {3}'.format(
                    self.executable, out_file, 
                    file, self._compile_flags)
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            self._link_list.append(out_file)
            counter += 1
        return 0

    def link_files(self):
        build_string = ''
        command('[LINK] {0}'.format(self.project_name))
        for file_name in self._link_list:
            build_string += ' {0}'.format(file_name)
        for item in self._link_flags:
            build_string += item
        try:
            os.makedirs(self.build_directory)
        except OSError:
            pass
        run_string = '{0} -o {1}/{2} {3}'.format(
                self.executable, self.build_directory,
                self.project_name, build_string)
        try:
            return_value = subprocess.call(run_string)
        except OSError:
            return_value = os.system(run_string)
        if not return_value == 0:
            return return_value
        return 0

    def add_define(self, define):
        self._compile_flags += format_options(define, '-D')

    def add_include_directory(self, directory):
        self._compile_flags += format_options(directory, '-I', True)

    def add_library_directory(self, directory):
        self._link_flags += format_options(directory, '-L', True)

    def add_library(self, library):
        self._link_flags += format_options(directory, '-l')

    @property
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        if isinstance(value, basestring):
            self._executable = which(value)

    @property
    def extensions(self):
        return ['.c']
