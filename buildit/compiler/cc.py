# Unix Based C Compiler

import os
import sys
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.language.c import C
from buildit.utils import format_options, fix_strings, file_hash
from buildit.cprint import command as print_command

class CC(Compiler):

    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self.executable = 'cc'
        self._language = C()

    def compile_files(self):
        counter = 1
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
            self._link_list.append(out_file)
            if os.path.exists(out_file) and \
                    hash == self.database.get_hash(file):
                self._file_list.remove(file)
            else:
                continue

        file_count = len(self._file_list)
        for file in self._file_list:
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
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
            if self._type == 'dynamic':
                self.add_compile_flags('-fPIC')
            run_string = '{0} -o "{1}" -c "{2}" {3}'.format(self.executable,
                    out_file, file, self._compile_flags)
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string) # Worst case scenario!
            if not return_value == 0:
                return return_value
            self.database.update_hash(file) # Let's write the hash
            counter += 1
        return 0

    def link_files(self):
        build_string = ''
        print_command('[LINK] {0}'.format(self._project_name))
        # Let's determine the final output!
        if self.type == 'binary':
            ending = ''
            if sys.platform == 'win32':
                ending = '.exe'
            elif sys.platform == 'darwin':
                ending = '.mac'
            else:
                ending = '.elf'
            self._project_name = '{0}{1}'.format(self._project_name, ending)
        elif self.type == 'static':
            self._project_name = 'lib{0}.a'.format(self._project_name)
            self.add_link_flags('-static')
        elif self.type == 'dynamic':
            ending = ''
            if sys.platform == 'win32':
                ending = '.dll'
            elif sys.platform == 'darwin':
                ending = '.dylib'
            else:
                ending = '.so'
            self._project_name = '{0}{1}'.format(self._project_name, ending)
            self.add_link_flags('-shared')
        else:
            return 1006 # Somehow our type was messed with :X
        for file in self._link_list:
            build_string += ' "{0}"'.format(file)
        for item in self._link_flags:
            build_string += item
        try:
            os.makedirs(self.build_directory)
        except OSError:
            pass
        run_string = '{0} -o "{1}/{2}" {3}'.format(self.executable,
                self.build_directory, self._project_name, build_string)
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
        self._link_flags += format_options(directory, '-I', True)

    def add_library_directory(self, directory):
        self._link_flags += format_options(directory, '-L', True)

    def add_library(self, library):
        self._link_flags += format_options(library, '-l')

    @property
    def C99(self):
        self.add_compile_flags('-std=c99')
        self.add_link_flags('-std=c99')
        
    @property
    def extensions(self):
        return ['.c']

    @property
    def enable_c(self):
        pass

    @property
    def module_extension(self):
        return ['.h']
