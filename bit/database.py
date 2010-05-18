# File Tracking Database

import os
import sys
import subprocess

from bit.utils import flatten, hash
from bit.cprint import error

class Database(object):

    def __init__(self, project_name, compiler_name):
        self.project_name = project_name
        self.compiler_name = compiler_name
        self.internal_dict = { }
        self.location = '.bit/{0}/{1}'.format(self.project_name, self.compiler_name)
        self.run
        dbfile = '{0}.hash'.format(self.location)
        if not os.path.exists(dbfile): open(dbfile, 'w+b').close()
        self.hashdb = open(dbfile, 'r+b')
        for line in self.hashdb:
            key, value = line.split('|')
            self.internal_dict[key] = value
        self.hashdb.close()


    def __del__(self):
        hashdb = open('{0}.hash'.format(self.location), 'w+b')
        for key, value in self.internal_dict.iteritems():
            hashdb.write('{0}|{1}\n'.format(key, value))
        hashdb.close()

    @property
    def run(self):
        try:
            os.makedirs(self.location)
            if sys.platform == 'win32':
                subprocess.call(['attrib', '+h', '.bit'])
        except OSError:
            pass

    def get_hash(self, file_name):
        if file_name in self.internal_dict:
            return self.internal_dict[file_name]
        return ''

    def update_hash(self, file_name, file_hash):
        self.internal_dict[file_name] = str(file_hash)
