# Utility functions for various actions

import os
import sys
import time
import shutil
import hashlib

import buildit

from buildit.cprint import error, warning

def file_hash(file_name):
    try: with open(file_name, 'rb') as f:
        h = hashlib.sha512()
        h.update(f.read())
        return str(h.hexdigest())
    except IOError:
        error('Could not hash: {0}'.format(file_name))

def is_exe(filepath):
    return os.path.exists(filepath) and os.access(filepath, os.X_OK)

def which(program_name):
    if buildit.windows:
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
    return 'echo'

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

# TODO: Possibly remove this
def lookup_error(value):
    error_value = {
                    None : 'Returned None',
                    1000 : 'File Copy Error',
                    1001 : 'Operating System Error',
                    1002 : 'Compiler Error',
                    1003 : 'Linker Error',
                    1004 : 'File IO Error',
                    1005 : 'Unable to remove directory',
                    1006 : 'Unknown Output Type',
                  }
    return error_value.get(value, 'Unknown Error')
