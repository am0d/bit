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
        # self.compiler = Compiler()
        self.__build_steps = []
        self._file_list = []
        self._type = 'binary'
        self._complete = False

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
        self.options.add_option('-d', '--directory', dest='base_directory',
                                default='.', help='Changes the base directory')
        buildit.parser.add_option_group(self.options)

    def __str__(self):
        return 'Platform'

    def run(self):
        start_time = datetime.now()
        for function in self.__build_steps:
            return_value = function()
            if not return_value:
                # TODO: Figure out how to get information here
                sys.exit(return_value)
        end_time - datetime.now()
        info('{0}|{1}: {2}'.format(self.project_name.upper(), self.name,
                                   (end_time - start_time))
        self._complete = True
        return 0

    def build(self): pass
        # TODO: WRITE THIS!
