import os.path

from buildit.hashdb import HashDB
from buildit.dependency.dependency import Dependency

from buildit.cprint import warning

class FileList:
    def __init__(self, project_name):
        self._file_list = []
        self._compile_list = []
        self._changed = {}
        self._have_compiled = {}
        self._extensions = []
        self._object_directory = '.'
        self._project_name = project_name
        self._hash_db = HashDB(self._project_name)
        self._deps_db = Dependency(self._project_name)

    def add(self, file_list):
        ''' Takes a list of files and adds them to the internal file list
            Arguments:
                - file_list: a list/tuple of files to add
        '''
        if isinstance(file_list, (tuple, list)):
            for file in file_list:
                if file not in self._file_list:
                    self._file_list.append(file)
                    if self._hash_db.has_changed(file):
                        self._changed[file] = True
                        self._have_compiled[file] = False
                        self.add_to_compile_list(file)
                        self._deps_db.parse_file(file)
                    else:
                        self._have_compiled[file] = True
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
                self._have_compiled[deps] = False
        
    def write_to_disk(self):
        ''' Saves the HashDb to file
        '''
        for file_name in self._have_compiled:
            if not self._have_compiled[file_name]:
                self._hash_db.remove_hash(file_name)
        self._hash_db.generate_hashfile()
        self._deps_db.write_to_disk()

    def set_extensions(self, extensions):
        ''' Sets the extensions that we will be compiling
        '''
        self._extensions = extensions

    def never_compile(self, extensions):
        ''' Marks files that we will never compile, but still depend on,
            as having been compiled already
        '''
        for file_name in self._compile_list:
            if file_name.endswith(tuple(extensions)):
                self._have_compiled[file_name] = True

    def have_compiled(self, file_name):
        ''' Records the file as having no errors
        '''
        self._have_compiled[file_name] = True

    def object_location(self, file_name):
        subdir = os.path.dirname(file_name)
        file_name = os.path.split(file_name)[1]
        location = '{0}/{1}/{2}.o'.format(self._object_directory,
                        subdir, file_name)
        return location

    @property
    def object_directory(self):
        return self._object_directory

    #@object_directory.setter
    def set_object_directory(self, value):
        self._object_directory = value

    @property
    def files_to_compile(self):
        return [file for file in self._compile_list
                if file.endswith(tuple(self._extensions))]

    @property
    def files_to_link(self):
        return [self.object_location(file) for file in self._file_list
                if file.endswith(tuple(self._extensions))]

    def set_language(self, language):
        ''' Sets the DepsDB to the correct language, and resets the
            compile_list to the correct values
        '''
        module = __import__("buildit")
        module = getattr(module, "dependency")
        module = getattr(module, language.lower())
        deps_class = getattr(module, language)
        self._deps_db = deps_class(self._project_name)

        self._compile_list = [i for i in self._changed]
        for file in self._changed:
            for dep in self._deps_db.get_files_dependent_on(file):
                if dep not in self._compile_list:
                    self._compile_list.append(dep)
