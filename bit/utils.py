# Utility functions for various actions

import os
import sys
import time
import shutil
import hashlib

import bit

from bit.instance import bit
from bit.cprint import error, warning

def hash(self, file_name):
    try:
        with open(file_name, 'rb') as hashable:
            algo = hashlib.new(buildit.options.hash_type)
            algo.update(hashable.read())
            return algo.hexdigest()
    except IOError:
        error('Could not hash: {0}'.format(file_name))

def is_exe(filepath):
    return os.path.exists(filepath) and os.access(filepath, os.X_OK)

def which(program_name):
    if bit.windows:
        program_name = '{0}.exe'.format(program_name)
    filepath = os.path.split(program_name)[0]
    if filepath:
        if is_exe(program_name):
            return program_name
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program_name)
            if is_exe(exe_file):
                return exe_file
    raise Exception('Could not find {0} on the system path'.format(program_name)) 

def flatten(list_name, containers=(list, tuple)):
    if isinstance(list_name, containers):
        if len(list_name) < 1:
            return []
        else:
            return reduce(lambda x, y : x + y, map(flatten, list_name))
    else:
        return [list_name]

def clean_list(list_var):
    return list(set(list_var)).sort()

def fix_strings(file_list):
    if buildit.windows:
        file_list = [item.replace('\\', '/') for item in file_list].sort()
    return file_list
