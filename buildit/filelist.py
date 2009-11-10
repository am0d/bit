from buildit.hashdb import HashDB
from buildit.dependency.dependency import Dependency

from buildit.cprint import warning

class FileList:
    def __init__(self, project_name):
        self._file_list = []
        self._compile_list = []
        self._hash_db = HashDB(project_name)
        self._deps_db = Dependency(project_name)

    def add(self, file_list):
        """ Takes a list of files and adds them to the internal file list
            Arguments:
                - file_list: a list/tuple of files to add
        """
        if isinstance(file_list, (tuple, list)):
            for file in file_list:
                if file not in self._file_list:
                    self._file_list.append(file)
                    if self._hash_db.has_changed(file):
                        self.add_to_compile_list(file)
        else:
            warning('{0} is not a supported type'.format(type(file_list)))

    def add_to_compile_list(self, file):
        """ Adds a file and all those that depend on it to the compile list
        """
        if file not in self._compile_list:
            self._compile_list.append(file)
        for deps in self._deps_db.get_files_dependent_on(file):
            if deps not in self._compile_list:
                self._compile_list.append(deps)
        
    def display(self):
        """ Displays the whole list of files
        """
        print self._file_list
