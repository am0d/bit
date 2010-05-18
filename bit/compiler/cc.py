# GCC Compiler
import os
import subprocess

import bit

from bit.compiler.compiler import Compiler
from bit.utils import flatten
from bit.cprint import command

class CC(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)
        self.compiler = 'cc'
        self.output_extension = 'o'
        self.cxx_support = False
        self.type = 'binary'

    def __str__(self):
        return 'CC'

    def compile_files(self):
        counter = 1
        if self.type == 'dynamic':
            self.add_compiler_flags('-fPIC')
        print self.file_list
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
            run_list = [self.compiler, '-o', '"{0}"'.format(out_file), '-c', 
                        '{0}'.format(file_name)] + self.compiler_flags
            self.format_command(percentage, info_file)
            try:
            #TODO FIXME
                raise OSError()
                #return_value = subprocess.call(run_list)
            except OSError:
                return_value = os.system(' '.join(run_list))
            if not return_value == 0:
                return return_value
            counter += 1
        return 0

    def link_files(self):
        if self.type == 'static':
            self.project_name = 'lib{0}.a'.format(self.project_name)
            self.add_linker_flags('-static')
        elif self.type == 'dynamic':
            self.project_name = 'lib{0}{1}'.format(self.project_name, self.link_extension)
            self.add_linker_flags('-shared')
        try:
            os.makedirs(self.build_directory)
        except OSError:
            pass
        run_list = flatten([self.compiler, '-o', '"{0}"'.format(self.project_name)] + self.link_list + self.linker_flags)
        command('[LINK] {0}'.format(self.project_name))
        print run_list
        try:
            subprocess.call(run_list)
        except OSError:
            os.system(' '.join(run_list))
        return 0

    def add_define(self, *defines):
        for define in flatten(list(set(defines))):
            self.add_compiler_flags('-D', define)

    def add_include_directory(self, *directories):
        for directory in flatten(list(set(directories))):
            self.add_compiler_flags('-I', directory)
            self.add_linker_flags('-I', directory)

    def add_library_directory(self, *directories):
        for directory in flatten(list(set(directories))):
            self.add_linker_flags('-L', directory)

    def add_library(self, *libraries):
        for library in flatten(list(set(libraries))):
            self.add_linker_flags('-l', library)

    @property
    def C99(self):
        self.add_compile_flags('-std=c99')
        self.add_linker_flags('-std=c99')

    @property
    def CXX(self):
        self.compiler = 'c++'
        self.cxx_support = True

    @property
    def extensions(self):
        item = ['.m', '.c']
        if self.cxx_support:
            item += ['.mm', '.cpp', '.cc', '.cxx', '.c++', '.C']
        return item

    @property 
    def link_extension(self):
        if bit.macosx:
            return '.dylib'
        elif bit.windows:
            return '.dll'
        else:
            return '.so'
