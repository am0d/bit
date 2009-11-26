# File Database Class
import anydbm

from buildit.utils import file_hash

class Database(object):

    def __init__(self, project_name, hash_type='sha512'):
        self.__project_name = project_name
        self.__language = None
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.__hashdb = anydb.open('{0}.hash'.format(self.__location), 'c')
        self.__depsdb = anydb.open('{0}.deps'.format(self.__location), 'c')
        self.__run()
        # We need to fill the hash_dictionary.

    def __del__(self):
        self.__hashdb.close()
        self.__depsdb.close()

    def __run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'win32':
                subprocess.call('attrib +h .buildit')
        except OSError:
            pass
        self.update_hash()

    # HashDB Functionality
    def add_hash(self, file_name):
        # More psuedo code than actually working (so don't use it!)
        hash = file_hash(file_name)

    def get_hash(self, file_name):
        # Ensure that the hash returned is a string.
        return str(self.hashdb[file_name])

    def update_hash(self, file_name):
        self.__hashdb[file_name] = file_hash(file_name)
        self.__hashdb.sync()

    def write_hash(self, file_list):
        for file_name in file_list:
            # Ensure that the hash stored is a string.
            self.__hashdb[file_name] = str(file_hash(file_name))
        self.__hashdb.sync()

    def write_deps(self, file_list):
        #for file_name in file_list:
        #    self.depsdb[file_name]
        self.__depsdb.sync()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, object):
            self.__language = value
