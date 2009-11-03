# Base Dependencies Class
''' The basic idea with this class is that it will parse (line by line) through
    every single file in the source directories (and local / non-system include
    directories), looking for lines similar to
    
    #include <file>
    #include "file"

    It will then parse the name of the file out of the include statement, and
    add it to the list of dependencies for the file currently being processed.
    This list will get written to a file called Depslist in the same directory
    as the build script.

    If, however, a file called Depslist already exists, this class will not
    parse through every single file.  Instead, it will use the list of files
    determined to have changed (by their hash list), and use this to decide 
    which files need to be re-parsed.  If a file has changed, it will be
    re-parsed.  If one of a file's dependencies has changed, the file will
    be added to the list of files to be re-compiled, but it will not be 
    re-parsed.
    '''

import os.path

from buildit.utils import which
from buildit.cprint import command

class Depslist(object):

    def __init__(self, include_dirs=[]):
        self.include_dirs=include_dirs
        self.current_file = ''

    def parse_line(self, line):
        ''' Parses one line to find the absolute path of any include
            statement on that line.
            '''
        line = line.strip()
        if line.startswith('#include '):
            line = line.replace('#include ', '', 1)
            line = line.replace('"', '')
            line = line.replace('<', '')
            line = line.replace('>', '')
            
            # search locally first e.g. "../test.h"
            current_dir = os.path.split(self.current_file)[0]
            path = '{0}/{1}'.format(current_dir, line)
            path = os.path.normpath(path)
            
            if os.path.exists(path):
                return path

            # we didn't find the file locally - 
            # lets see if it is in one of the include directories
            for dir in self.include_dirs:
                path = '{0}/{1}'.format(dir, line)
                if os.path.exists(path):
                    return path

            # didn't find the file, return blank
            # this should probably happen for all system includes
            return ''
        else:
            return ''

    def parse_file(self, file):
        ''' Parses one file and returns a list of all the files
            that the file depends on (determined by the files it
            includes).
            '''
        deps = []
        try:
            file = open(file, "r")
            try:
                self.current_file = file.name

                for line in file:
                    path = self.parse_line(line)
                    if not path == '':
                        deps.append(path)
            finally:
                file.close()
                return deps
        except IOError:
            return deps

    def get_dependencies(self, file):
        ''' Returns a list of all the files that depend on file
            '''
        pass

    def get_changed_files(self, file_list):
        ''' Iterates through the list of files that have changed,
            and adds any files that depend on them.
            '''
        for file in file_list:
            deps_list = self.get_dependencies(file)

            for dependency in deps_list:
                if not dependency in file_list:
                    file_list.add(dependency)

