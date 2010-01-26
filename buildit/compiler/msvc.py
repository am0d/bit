import os
import sys
import subprocess
from buildit.compiler.compiler import Compiler
from buildit.language.cpp import CPP
from buildit.utils import format_options, fix_strings, file_hash
from buildit.cprint import command as print_command

class MSVC(Compiler):
    def __init__(self, project_name='PROJECT'):
        Compiler.__init__(self, project_name)
        self._clang_enabled = False
        self.__exception_handler = False
        self.executable = 'cl'
        self._language = CXX()

    def __str__(self):
        return 'MSVC'

    def setup_files(self):
        self.__file_count = len(self._file_list)
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}.obj'.format(self.object_directory, file)
            if os.path.exists(out_file) and \
                    hash == self.database.get_hash(file):
                try: 
                    self._file_list.remove(file)
                except ValueError:
                    pass
                self._link_list.append(out_file)
                self.__file_count -= 1
                continue
        self._file_list.sort()
        return 0

    def compile_files(self):
        counter = 1
        for file in self._file_list:
            out_file = '{0}/{1}.obj'.format(self.object_directory, file)
            percentage = self.percentage(counter, self.__file_count)
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
            if self.__exception_handler:
                self._compile_flags += ' /EHa'
            run_string = '{0} /nologo /Fo "{1}" /c "{2}" {3}'.format(
                self.executable, out_file, file, self._compile_flags)
            if len(run_string) > 1024:
                raise OSError('MSVC supports a maximum of 1024 characters')
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string)
            if not return_value == 0:
                return return_value
            self.database.update_hash(file)
            self._link_list.append(file)
            counter +=1
        return 0
    
    def link_files(self):
        build_string = ''
        print_command('[LINK] {0}'.format(self._project_name))
        # Let's determine the final output!
        self.executable = 'link'
        if self.type == 'binary':
            ending = '.exe'
            self._project_name = '{0}{1}'.format(self._project_name, ending)
        elif self.type == 'dynamic':
            ending = '.dll'
            self._project_name = '{0}{1}'.format(self._project_name, ending)
            self.add_link_flags('/LD')
        elif self.type == 'static':
            self._project_name = '{0}.lib'.format(self._project_name)
            self.executable = 'lib'
        else:
            return 1006 # Somehow our type was messed with :X
        build_string += ''.join(self._link_flags)
        for file in self._link_list:
            build_string += ' "{0}"'.format(file)
        try:
            os.makedirs(self.build_directory)
        except OSError:
            pass
        run_string = '{0} /nologo /OUT:"{1}/{2}" {3}'.format(self.executable,
                self.build_directory, self._project_name, build_string)
        try:
            return_value = subprocess.call(run_string)
        except OSError:
            return_value = os.system(run_string)
        if not return_value == 0:
            return return_value
        return 0

    def add_define(self, *defines):
        self._compile_flags += format_options(define, '/D')

    def add_include_directory(self, *directories):
        directories = flatten(list(directories))
        for directory in directories:
            self._compile_flags += format_options(directory, '/I', True)

    def add_library_directory(self, *directories):
        directories = flatten(list(directories))
        path_list = []
        for path in os.environ['LIB'].split(os.pathsep):
            path_list.append(path)
        for directory in directories:
            path_list.append(directory)
        path_list = os.pathsep.join(path_list)
        os.environ['LIB'] = path_list

    def add_library(self, library):
        self._link_flags += format_options(library, '-l')

    @property
    def C99(self):
        pass
        
    @property
    def extensions(self):
        if not self._clang_enabled:
            return ['.cpp', '.cc', '.cxx', '.c++', '.C']
        else:
            return ['.c', '.cc', '.cpp', '.cxx', '.c++', '.C']

    @property
    def enable_c(self):
        self._clang_enabled = True

    @property
    def exceptio_handler(self):
        self.__exception_hadnler = True

    @property
    def module_extension(self):
        return ['.h', '.hpp', '.hxx', '.h++']
