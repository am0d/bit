from buildit.hashdb import HashDB
from buildit.dependency.dependency import Dependency

from buildit.cprint import warning

class FileList:
    def __init__(self, project_name):
        self._file_list = []
        self._compile_list = []
        self._has_errors = {}
        self._extensions = []
        self._hash_db = HashDB(project_name)
        self._deps_db = Dependency(project_name)

    def add(self, file_list):
        ''' Takes a list of files and adds them to the internal file list
            Arguments:
                - file_list: a list/tuple of files to add
        '''
        if isinstance(file_list, (tuple, list)):
            for file in file_list:
                if file not in self._file_list:
                    self._file_list.append(file)
                    self._has_errors[file] = True
                    if self._hash_db.has_changed(file):
                        self.add_to_compile_list(file)
        else:
            warning('{0} is not a supported type'.format(type(file_list)))

    def add_to_compile_list(self, file):
        ''' Adds a file and all those that depend on it to the compile list
        '''
        if file not in self._compile_list:
            self._compile_list.append(file)
        for deps in self._deps_db.get_files_dependent_on(file):
            if deps not in self._compile_list:
                self._compile_list.append(deps)
                if deps not in self._has_errors:
                    self._has_errors[deps] = True
        
    def write_to_disk(self):
        ''' Saves the HashDb to file
        '''
        for file_name in self._has_errors:
            if self._has_errors[file_name]:
                self._hash_db.remove_hash(file_name)
        self._hash_db.generate_hashfile()

    def set_extensions(self, extensions):
        self._extensions = extensions

    def has_no_errors(self, file_name):
        ''' Records the file as having no errors
        '''
        self._has_errors[file_name] = False

    @property
    def files_to_compile(self):
        return [file for file in self._compile_list
                if file.endswith(tuple(self._extensions))]

    @property
    def files_to_link(self):
        return [file for file in self._file_list
                if file.endswith(tuple(self._extensions))]
