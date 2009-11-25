# File Database Class
# Scons does this as well, from what I understand.

import sqlite3

from buildit.utils import file_hash

class Database(object):

    def __init__(self, project_name, hash_type='sha512'):
        self.__project_name = project_name
        self.__language = None
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.__connection = sqlite3.connect(self.__location)
        self.__hash_dictionary = {}
        self.__run()
        # We need to fill the hash_dictionary.


    def __run(self):
        try:
            os.makedirs('.buildit')
            if sys.platform == 'win32':
                subprocess.call('attrib +h .buildit')
        except:
            pass
        self.update_hash()

    # HashDB Functionality
    def add_hash(self, file_name):
        # More psuedo code than actually working (so don't use it!)
        cursor = self.__connection.cursor()
        hash = file_hash(file_name)
        cursor.execute('insert into hashes values (?, ?)', file_name, hash)
        cursor.close()

    def get_hash(self, file_name):
        if file_name in self.__hash_dictionary:
            return self.__hash_dictionary[file_name]

    def remove_hash(self, file_name):
        if file_name in self.__hash_dictionary:
            del self.__hash_dictionary[file_name]

    def update_hash(self):
        file_hash = []
        cursor = self.__connection.cursor()
        cursor.execute('select * from hashes')
        for file, hash in cursor:
            file_hash.append((file, hash))
        cursor.close()
        # A straight list -> dict conversion fails sometimes.
        # list -> tuple -> dict seems to work.
        self.__hash_dictionary = dict(tuple(file_hash))

    def write(self, file_list):
        cursor = self.__connection.cursor()
        cursor.close()

    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, object):
            self.__language = value
