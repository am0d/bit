# File Database Class
# Scons does this as well, from what I understand.

import sqlite3

from buildit.utils import file_hash

class Database(object):

    def __init__(self, project_name):
        self.__project_name = project_name
        self.__location = '.buildit/{0}'.format(self.__project_name)
        self.__connection = sqlite3.connect(self.__location)
        self.__cursor = self.__connection.cursor()
        self.__dependency = None

    def add_hash(self, file_name):
        # More psuedo code than actualy working (so don't use it!)
        hash = file_hash(file_name)
        self.__cursor.execute('insert into hash values(?)', (file_name, hash))
    
    def write(self):
        pass

    @property
    def dependency(self):
        return self.__dependency

    @dependency.setter
    def dependency(self, value):
    
