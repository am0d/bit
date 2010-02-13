# Unix Based C Compiler

import os
import sys
import shutil
import subprocess

from buildit.compiler.compiler import Compiler
from buildit.utils import format_options, fix_strings, file_hash, flatten
from buildit.cprint import command as print_command


class CC(Compiler):

    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self.executable = 'cc'
        self._cxx_support = False
        self._clang_enabled = False

    def __str__(self):
        if not self._cxx_support:
            return 'CC'
        return 'CXX'

    def setup_files(self):
        self._file_list = flatten(self._file_list)
        self.__file_count = len(self._file_list)
        compile_list = []
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
            if os.path.exists(out_file) and \
                    hash == self.database.get_hash(file):
                self._link_list.append(out_file)
                self.__file_count -= 1
            else:
                compile_list.append(file)
        self._file_list = compile_list
        self._file_list.sort()
        return 0

    def compile_files(self):
        counter = 1
        for file in self._file_list:
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
            percentage = self._percentage(counter, self.__file_count)
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
            except OSError: # It's alright if the directory already exists.
                pass
            self.command(percentage, info_file)
            if self._type == 'dynamic':
                self.add_compiler.flags('-fPIC')
            run_string = '{0} -o "{1}" -c "{2}" {3}'.format(self.executable, 
                         out_file, file, self._compile_flags)
            # Unfortunately, due to some bizarre bugs, properly calling this on 
            # Unix systems will not work properly, hence the os.systenm call.
            # subprocess *does* work on windows however. 
            # (A simple run_string.split(' ') should have worked, 
            # but alas it does not. 
            # g++ does not care for quoted files via a list :/
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            self.database.update_hash(file) # Fix up that hash, yo!
            self._link_list.append(file)
            counter += 1
        return 0

    def link_files(self):
        build_string = ''
        print_command('[LINK] {0}'.format(self._project_name))
        # We need to determine the final output
        if self.type =='binary':
            self.project_name = '{0}{1}'.format(self._project_name, 
                    self._output_extension)
        elif self.type == 'static':
            self._project_name = 'lib{0}.a'.format(self._project_name)
            self.add_link_flags('-static')
        elif self.type == 'dynamic':
            self._project_name = 'lib{0}{1}'.format(self._project_name, 
                    self._output_extension)
            self.add_link_flags('-shared')
        else:
            return 1006 # Somehow our type was messed with :X
        for file in self._link_list:
            build_string += ' "{0}"'.format(file)
        for item in self._link_flags:
            build_string += item
        try:
            os.makedirs(self.build_directory)
        except:
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

    def add_define(self, *defines):
        defines = flatten(list(defines))
        for define in defines:
            self._compile_flags += format_options(define, '-D')

    def add_include_directory(self, *directories):
        directories = flatten(list(directories))
        for directory in directories:
            self._compile_flags += format_options(directory, '-I', True)
            self._link_flags += format_options(directory, '-I', True)

    def add_library_directory(self, *directories):
        directories = flatten(list(directories))
        for directory in directories:
            self._link_flags += format_options(directory, '-L', True)

    def add_library(self, *libraries):
        libraries = flatten(list(libraries))
        for library in libraries:
            self._link_flags += format_options(library, '-l')

    @property
    def C99(self):
        self.add_compile_flags('-std=c99')
        self.add_link_flags('-std=c99')
    
    @property 
    def CXX(self):
        self.executable = 'c++'
        self._cxx_support = True

    @property
    def extensions(self):
        if not self._cxx_support:
            item =  ['.c']
        else:
            item = ['.cpp', '.cc', '.cxx', '.c++', '.C']
            if self._clang_enabled:
                item.append('.c')
        return item + self.user_extensions

    @property
    def enable_c(self):
        if self._cxx_support:
            self._clang_enabled = True

    @property
    def dependency_extension(self):
        if not self._cxx_support:
            item = ['.h'] 
        else:
            item = ['.h', '.hpp', '.hxx', '.h++']
        return item + self.user_dependencies
