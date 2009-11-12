# File Database Class
# Scons does this as well, from what I understand.

import sqlite3

class Database(object):

    def __init(self, project_name):
        self.__project_name = project_name
        self.__location = '.buildit/{0}'.format(self.__project_name)
