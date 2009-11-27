# Unix Based C Compiler

import os
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.utils import which, file_hash, format_options, fix_strings
from buildit.cprint import command

class CC(Compiler):

    def __init__(self):
        Compiler.__init__(self)
        self._executable = which('cc') 
        self._language = 'C'

    def compile_files(self):
        counter = 1
        file_count = 0 #len(self._file_list.files_to_compile)
        file_list = [] #self._file_list.files_to_compile
        for file in file_list:
            percentage = self._percentage(counter, file_count)
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
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
            self._info_string(percentage, info_file)
            run_string = '{0} -o "{1}" -c "{2}" {3}'.format(
                    self.executable, out_file,
                    file, self._compile_flags)
            try:
                return_value = subprocess.call(run_string) 
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            self._file_list.have_compiled(file)
            counter += 1
        return 0

    def link_files(self):
        build_string = ''
        command('[LINK] {0}'.format(self._project_name))
        for file_name in []: #self._file_list.files_to_link:
            build_string += ' "{0}/{1}"'.format(self.object_directory, 
                    file_name)
        for item in self._link_flags:
            build_string += item
        try:
            os.makedirs(self.build_directory)
        except OSError:
            pass
        run_string = '{0} -o "{1}/{2}" {3}'.format(
                self.executable, self.build_directory,
                self._project_name, build_string)
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

    @property
    def never_compile(self):
        return ['.h']
