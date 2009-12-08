# Base Compiler Class

import os
import subprocess

from buildit.language.generic import Generic
from buildit.database import Database

from buildit.utils import which, flatten, fix_strings, file_hash
from buildit.utils import format_options
from buildit.utils import name as uname
from buildit.cprint import command as print_command

class Compiler(object):

    def __init__(self, project_name='PROJECT'):
        self._compile_steps = []
        self._type = 'binary'
        self._language = Generic()
        self._project_name = project_name
        self._compile_flags = ''
        self._link_flags = ''
        self._executable = which('echo')
        self._file_list = []
        self._link_list = []

        self._compile_steps.append(self.setup_files)
        self._compile_steps.append(self.compile_files)
        self._compile_steps.append(self.link_files)

    @property
    def run(self):
        self.database = Database(self._project_name, self._language)
        for function in self._compile_steps:
            return_value = function()
            if not return_value == 0:
                return return_value
        return 0

    def setup_files(self):
        return 0

    # Leave the implementation up to each compiler
    def compile_files(self):
        counter = 1
        compile_list = []
        for file in self._file_list:
            hash = file_hash(file)
            out_file = '{0}/{1}.o'.format(self.object_directory, file)
            if os.path.exists(out_file) and \
                    hash == self.database.get_hash(file):
                self._link_list.append(out_file)
            else:
                if file not in compile_list:
                    compile_list.append(file)
                for dep in self.database.get_deps(file):
                    if dep not in compile_list:
                        compile_list.append(dep)
        file_count = len(compile_list)
        for file in compile_list:
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
            self.command(percentage, info_file)
            run_string = '{0} {1} {2}'.format(self.executable,
                    self.compile_string(out_file, file), self._compile_flags)
            try:
                return_value = subprocess.call(run_string)
            except OSError:
                return_value = os.system(run_string) # Worst case scenario!
            if not return_value == 0:
                return return_value
            self.database.update_hash(file) # Let's write the hash
            self._link_list.append(out_file)
            counter += 1
        return 0

    def compile_string(self, output_file, input_file):
        pass

    def link_files(self):
        return 0

    def _percentage(self, counter, list_length):
        percentage = 100 * float(counter)/float(list_length)
        percentage = str(percentage).split('.')
        percentage = percentage.pop(0)
        return percentage

    def command(self, percentage, file_name):
        print_command('[{0:>3}%] {1}: {2}'.format(percentage, 
            self.name.upper(), file_name))

    def add_flags(self, flags):
        self._compile_flags += format_options(flags)

    def add_compile_flags(self, flags):
        self._compile_flags += format_options(flags)

    def add_link_flags(self, flags):
        self._link_flags += format_options(flags)

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
        return ['.txt']

    @property
    def name(self):
        return uname(self)
