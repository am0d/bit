# Base Compiler Class

import os
import subprocess

from buildit.database import Database

from buildit.utils import which, flatten, fix_strings, file_hash
from buildit.utils import format_options
from buildit.cprint import command as print_command

class Compiler(object):

    def __init__(self, project_name='PROJECT'):
        self._compile_steps = []
        self._type = 'binary'
        self._output_extension = '' # We normally won't have one.
        self._project_name = project_name
        self._compile_flags = ''
        self._link_flags = ''
        self._executable = which('echo')
        self._file_list = []
        self._link_list = []
        self._dependency_folder_list = []
        self._dependency_file_list = []
        self.user_extensions = []
        self.user_dependencies = []

        self._compile_steps.append(self.setup_files)
        self._compile_steps.append(self.compile_files)
        self._compile_steps.append(self.link_files)
        self._compile_steps.append(self.write_deps)

    def __str__(self):
        return 'Compiler'

    @property
    def run(self):
        self.database = Database(self._project_name)
        for function in self._compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0

    def setup_files(self):
        return 0

    # Leave the implementation up to each compiler
    def compile_files(self):
        return 0

    def link_files(self):
        return 0

    def parse_deps(self):
        # We want this to run first
        self._compile_steps.insert(0, self.dependency_tracking)
        return 0
    
    def dependency_tracking(self):
        for folder in self._dependency_folder_list:
            if not os.path.isdir(folder):
                continue
            glob_list = []
            for root, dir, file_names in os.walk(folder):
                for extension in flatten(self.dependency_extensions):
                    glob_list += glob('{0}/*{1}'.format(root, extension))
            glob_list = fix_strings(glob_list)
            for file_name in glob_list:
                self._dependency_file_list.append(file_name)
        self._dependency_file_list.sort()
        return 0

    def write_deps(self):
        # This runs last (Basically writes our dependency_file_list to disk)
        return 0

    def _percentage(self, counter, list_length):
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.')
        percentage = percentage.pop(0)
        return percentage

    def command(self, percentage, file_name):
        print_command('[{0:>3}%] {1}: {2}'.format(percentage, 
            self.name.upper(), file_name))

    def add_flags(self, *flags):
        flags = flatten(list(flags))
        for flag in flags:
            self._compile_flags += format_options(flag)

    def add_compile_flags(self, *flags):
        flags = flatten(list(flags))
        for flag in flags:
            self._compile_flags += format_options(flag)

    def add_link_flags(self, *flags):
        flags = flatten(list(flags))
        for flag in flags:
            self._link_flags += format_options(flag)

    def add_dependency_folder(self, *folders):
        folders = flatten(list(folders))
        for folder in folders:
            self._dependency_list.append(folder)

    def add_file_extension(self, *extensions):
        extensions = flatten(list(extensions))
        for extension in extensions:
            extension = extension.split('.')
            if len(extension) > 1:
                extension = '.'.join(extension)
            else:
                extension = extension.pop()
            self.user_extensions.append('.{0}'.format(extension))

    def add_dependency_extension(self, *extensions):
        extensions = flatten(list(extensions))
        for extension in extensions:
            extension = extension.split('.')
            if len(extension) > 1:
                extension = '.'.join(extension)
            else:
                extension = extension.pop()
            self.user_dependencies.append('.{0}'.format(extension))

    @property
    def output_extension(self):
        return self._output_extension

    @output_extension.setter
    def output_extension(self, value):
        self._output_extension = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def language(self):
        return self._language

    @property 
    def executable(self):
        return self._executable

    @executable.setter
    def executable(self, value):
        if isinstance(value, basestring):
            self._executable = which(value)

    @property
    def build_directory(self):
        return self._build_directory

    @build_directory.setter
    def build_directory(self, value):
        self._build_directory = value

    @property
    def object_directory(self):
        return self._object_directory

    @object_directory.setter
    def object_directory(self, value):
        self._object_directory = value

    @property
    def extensions(self):
        return ['.txt'] + self.user_extensions

    @property
    def dependency_extensions(self):
        return ['.txt'] + self.user_dependencies

    @property
    def name(self):
        return self.__str__()
