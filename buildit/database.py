# File Database Class
# Scons does this as well, from what I understand.
import anydbm

from buildit.utils import file_hash

class Database(object):

    def __init__(self, project_name, hash_type='sha512'):
        self.__project_name = project_name
        self.__language = None
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.hashdb = anydb.open(self.__location, 'c')
        
        self.__run()
        # We need to fill the hash_dictionary.


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
        if file_name in self.__hash_dictionary:
            return self.__hash_dictionary[file_name]

    def remove_hash(self, file_name):
        if file_name in self.__hash_dictionary:
            del self.__hash_dictionary[file_name]

    def update_hash(self):
        file_hash = []
        # A straight list -> dict conversion fails sometimes.
        # list -> tuple -> dict seems to work.
        self.__hash_dictionary = dict(tuple(file_hash))

    def write(self, file_list):
        pass

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, object):
            self.__language = value
