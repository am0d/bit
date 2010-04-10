# File Hash type that allows for a constant hash type for all databases.

import hashlib

import buildit.buildit as buildit

from buildit.harbinger import Harbinger
from buildit.cprint import error

class FileHash(Harbinger):

    def __init__(self):
        Harbinger.__init__(self)
        self.hash_algo = hashlib.new(buildit.options.hash_type)

    def hash(self, file_name):
        try: 
            with open(file_name, 'rb') as f:
                self.hash_algo.update(f.read())
                return str(self.hash_algo.hexdigest())
        except IOError:
            error('Could not hash: {0}'.format(file_name))

file_hash = FileHash()
