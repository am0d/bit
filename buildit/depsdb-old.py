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
from buildit.cprint import command, warning

class DepsDB(object):

    def __init__(self, project_name, include_dirs=[]):
        ''' Initialise all the attributes and load any pre-calculated
            dependencies into memory
            '''
        self.include_dirs = include_dirs
        self.project_name = project_name
        self.__location = '.buildit/{0}.deps'.format(
                            self.project_name)
        self.__dependencies = {}
        self.__run()

    def parse_line(self, line, current_file):
        ''' Parses one line to find the absolute path of any include
            statement on that line.
            '''
        line = line.strip()
        if line.startswith('#include '):
            line = line.replace('#include ', '', 1)
            line = line.replace('"', '')
            line = line.replace('<', '')
            name = line.replace('>', '')
            
            # search locally first e.g. "../test.h"
            current_dir = os.path.split(current_file)[0]
            path = '{0}/{1}'.format(current_dir, name)
            path = os.path.normpath(path)
            
            if os.path.exists(path):
                return path

            # we didn't find the file locally - 
            # lets see if it is in one of the include directories
            for dir in self.include_dirs:
                path = '{0}/{1}'.format(dir, name)
                if os.path.exists(path):
                    return path

            # didn't find the file, return blank
            # this should probably happen for all system includes
            return ''
        else:
            return ''

    def parse_file(self, file_name):
        ''' Parses one file and returns a list of all the files
            that the file depends on (determined by the files it
            includes).
            '''
        deps = []
        try:
            file = open(file_name, "r")
            try:
                for line in file:
                    path = self.parse_line(line, file_name)
                    if not path == '':
                        deps.append(path)
            finally:
                file.close()
        except IOError:
            pass
        for name in deps:
            if name not in self.__dependencies:
                self.__dependencies[name] = []
            if file_name not in self.__dependencies[name]:
                self.__dependencies[name].append(file_name)
        return deps

    def get_dependencies(self, file):
        ''' Returns a list of all the files that depend on file
            '''
        return self.__dependencies.get(file, [])

    def get_changed_files(self, file_list):
        ''' Iterates through the list of files that have changed,
            and adds any files that depend on them.
            '''
        for file in file_list:
            deps_list = self.get_dependencies(file)

            for dependency in deps_list:
                if not dependency in file_list:
                    file_list.add(dependency)

    def __run(self):
        ''' Load into memory all the files currently in the dependency
            graph on disk
            '''
        try:
            # make sure we have a .buildit directory
            os.makedirs('.buildit/')
            if system_type() == 'windows':
                subprocess.call('attrib +h .buildit')
        except:
            pass
        if not os.path.exists(self.__location):
            # create the .deps file if it doesn't exist already
            warning('Dependency graph not found. Running first time '\
                    'generation')
            try:
                self.deps_file = open(self.__location, 'w')
                self.deps_file.close()
            except IOError:
                pass
        try:
            #read in all the dependencies from the file
            self.deps_file = open(self.__location)
            for line in self.deps_file:
                line = line.replace('\n', '')
                line = line.split(':')
                if line[0] not in self.__dependencies:
                    self.__dependencies[line[0]] = []
                self.__dependencies[line[0]].append(line[1])
            self.deps_file.close()
        except IOError:
            pass

    def save_deps(self):
        try:
            self.deps_file = open(self.__location, 'w')
            for file, deps in self.__dependencies.iteritems():
                for dep in deps:
                    self.deps_file.write('{0}:{1}\n'.format(file, dep))
        except:
            warning('An error occurred while saving the dependency graph')
