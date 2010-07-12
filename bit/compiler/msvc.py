# MSVC Compiler

import os
import subprocess 

from bit.compiler.compiler import Compiler
from bit.utils import flatten, hash
from bit.cprint import command, error

class MSVCCompiler(Compiler):

    def __init__(self, project_name):
        Compiler.__init__(self, project_name)
        self.c_support = False
        self.output_extension = 'obj'
        self.type = 'binary'

    def __str__(self):
        return 'MSVC'

    def compile_files(self):
        self.executable = 'cl'
        counter = 1
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
            except OSError:
                pass 
            run_list = [self.executable, '/nologo', '/EHsc', '/Fo"{0}"'.format(out_file), '/c', '"{0}"'.format(file_name)] + self.compiler_flags
            self.format_command(percentage, info_file)
            run_list = ' '.join(run_list)
            try:
                return_value = subprocess.call(run_list)
            except OSError:
                return_value = os.system(run_list)
            if not return_value:
                return return_value
            self.link_list.append(out_file)
            counter += 1
        return 0

    def link_files(self):
        if self.type == 'static':
            self.executable = 'lib'
            out_comm = '/OUT:{0}/{1}.lib'.format(self.build_directory, self.project_name)
        elif self.type == 'dynamic':
            self.lflags('/LD'), self.lflags('/DLL'), self.lflags('/link')
            out_comm = '/OUT:{0}/{1}.dll'.format(self.build_directory, self.project_name)
        else:
            self.lflags('/Fe"{0}/{1}.exe"'.format(self.build_directory, self.project_name))
            out_comm = [ ]
        run_list = flatten([self.executable, '/nologo'] + self.link_list + self.linker_flags + [out_comm])
        run_list = ' '.join(run_list)
        command('[LINK] {0}'.format(self.project_name))
        try:
            subprocess.call(run_list)
        except OSError:
            os.system(run_list)
        return 0

    def define(self, *defines):
        for define in flatten(list(set(defines))):
            self.cflags('/D', define)

    def incdir(self, *directories):
        for directory in flatten(list(set(directories))):
            self.cflags('/I', directory)

    def libdir(self, *directories):
        path_list = [path for path in os.environ['LIB'].split(os.pathsep)]
        for directory in flatten(list(set(directories))):
            path_list.append(directory)
        os.environ['LIB'] = os.pathsep.join(path_list)

    def library(self, *libraries):
        for library in flatten(list(set(libraries))):
            self.lflags('{0}.lib'.format(library))

    @property
    def enable_c(self):
        self.c_support = True

    @property 
    def extensions(self):
        item = ['.cpp', '.cc', '.cxx', '.c++']
        if self.c_support:
            item.append('.c')
        return item

