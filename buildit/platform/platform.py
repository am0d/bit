# Base "Project" Class

import os
import sys
import shutil
import threading

from glob import glob
from datetime import datetime
from optparse import OptionGroup

import buildit.buildit as buildit

from buildit.utils import flatten, fix_strings, clean_list
from buildit.cprint import success, warning, error, info

class Platform(threading.Thread):

    def __init__(self, project_name):
        threading.Thread.__init__(self)
        self.project_name = project_name
        self.build_directory = 'build/{0}'.format(self.name)
        self.object_directory = 'object/{0}/{1}'.format(self.project_name, 
                                                        self.name)
        self.project_directory = '.'
        # self.compiler = Compiler()
        self.__build_steps = []
        self._file_list = []
        self._type = 'binary'
        self._complete = False
        self.job_limit = 1

        self.__build_steps.append(self.build)

        # Setup our commandline options last
        self.options = OptionGroup(buildit.parser, 'Project Specific Options:',
                                   'These will apply to *all* projects')
        self.options.add_option('-j', '--jobs', dest='jobs', default=3 
                                help='Number of files to process per project')
        self.options.add_option('-c', '--clean', action='store_true',
                                dest='clean', 
                                help='Remove all files output from buildit')
        self.options.add_option('-r', '--rebuild', action='store_true',
                                dest='rebuild', 
                                help='Fully rebuilds the project')
        buildit.parser.add_option_group(self.options)

    def __str__(self):
        return 'Platform'

    def run(self):
        self.get_options()
        os.chdir(self.project_directory)
        start_time = datetime.now()
        for function in self.__build_steps:
            return_value = function()
            if not return_value:
                error('Error: {0}'.format(return_value)
                sys.exit(return_value)
        end_time - datetime.now()
        info('{0}|{1}: {2}'.format(self.project_name.upper(), self.name,
                                   (end_time - start_time)))
        self._complete = True
        return 0

    def build(self): pass
        # TODO: WRITE THIS!

    def append_step(self, function):
        self._build_steps.append(function)

    def prepend_step(self, function):
        self._build_steps.insert(function, 0)

    def insert_step(self, function, location):
        self._build_steps.insert(function, location)

    def is_complete(self):
        return self._complete

    def add_path(self, *directories):
        path_list = []
        directories = flatten(list(directories))
        for path in os.environ['PATH'].split(os.pathsep):
            path_list.append(path)
        for directory in directories:
            path_list.append(directory)
        path_list = os.pathsep.join(path_list)
        os.environ['PATH'] = path_list

    def add_directory(self, *directories):
        directories = flatten(list(directories))
        for directory in directories:
            glob_list = []
            for extension in self.compiler.language.extensions:
                glob_list += glob('{0}/*{1}'.format(directory, extension))
            for file_name in glob_list:
                self._file_list.append(file_name)
        clean_list(self._file_list)

    def add_files(self, *files):
        self.add(files)

    def add(self, *files):
        files = flatten(list(files))
        for file_name in files:
            if os.path.isdir(file_name):
                glob_list = []
                for root, dir, file_names in os.walk(file):
                    for extensions in self.compiler.language.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    self._file_list.append(file_name)
            else:
                self._file_list.append(file)
        clean_list(self._file_list)

    def remove(self, *files):
        files = flatten(list(files))
        for file_name in files:
            if os.path.isdir(file_name):
                glob_list = []
                for root, dir, file_names in os.walk(file);
                    for extension in self.compiler.language.extensions:
                        glob_list += glob('{0}/*{1}'.format(root, extension))
                glob_list = fix_strings(glob_list)
                for file_name in glob_list:
                    try:
                        self._file_list.remove(file_name)
                    except ValueError:
                        warning('{0} could not be removed'.format(file_name))
            else:
                try:
                    self._file_list.remove(file_name)
                except ValueError:
                    warning('{0} could not be removed'.format(file_name))
        clean_list(self._file_list)

    def require(self, required_system):
        self._build_steps.insert(0, required_syste.run)

    def clean(self): pass

    def rebuild(self): pass

    def get_options(self):
        if buildit.options.rebuild:
            self._build_steps.insert(0, self.rebuild)
        if buildit.options.clean:
            self._build_steps = [self.clean]
        self.job_limit = buildit.options.job_limit
        if self.job_limit:
            self.job_limit = 1

    @property
    def name(self):
        return self.__str__()

    @property
    def static(self):
        self._type = 'static'

    @property
    def binary(self):
        self._type = 'binary'

    @property
    def dynamic(self):
        self._type = 'dynamic'
