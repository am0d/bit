from buildit.hashdb import HashDB
from buildit.dependency.dependency import Dependency

from buildit.cprint import warning

class FileList:
    def __init__(self, project_name):
        self._file_list = []
        self._hash_db = HashDB(project_name)
        self._deps_db = Dependency(project_name)

    def add(self, file_list):
        """ Takes a list of files and adds them to the internal file list
        """
        if isinstance(file_list, (tuple, list)):
            for file in file_list:
                if file not in self._file_list:
                    self._file_list.append(file)
        else:
            warning('{0} is not a supported type'.format(type(file_list)))

    def display(self):
        print self._file_list
