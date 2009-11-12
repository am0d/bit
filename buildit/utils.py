# Utility functions for various actions

import os
import sys
import time
import shutil
import tarfile
import zipfile
import hashlib
import threading
import os.path

from buildit.cprint import error, warning

def wait():
    while threading.active_count() > 1:
        time.sleep(1)

def file_hash(file_name):
    try:
        f = open(file_name, 'rb')
        h = hashlib.sha512()
        h.update(f.read())
        f.close()
        return h.hexdigest()
    except IOError:
        error('Could not hash: {0}'.format(file_name))

def is_exe(filepath):
    return os.path.exists(filepath) and os.access(filepath, os.X_OK)

def which(program_name):
    if sys.platform == 'win32':
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
    return None

def flatten(list_name, containers=(list, tuple)):
    if isinstance(list_name, containers):
        if len(list_name) < 1:
            return []
        else:
            return reduce(lambda x, y : x + y, map(flatten, list_name))
    else:
        return [list_name]

def fix_strings(file_list): #Really should only be used internally
    if isinstance(file_list, list) or isinstance(file_list, tuple):
        if sys.platform == 'windows':
           file_list = [file_name.replace('\\', '/') 
                        for file_name in file_list ]
        file_list.sort()
    return file_list

def format_options(option_list, option='', quotes=False):
    string = ''
    if isinstance(option_list, basestring):
        option_list = [option_list]
    else:
        option_list = list(option_list)
        option_list = flatten(option_list)
    for item in option_list:
        if quotes:
            item = '"{0}"'.format(item)
        string += ' {0}{1}'.format(option , item)
    return string
    
def lookup_error(value):
    error_value = {
                    None : 'Returned None',
                    1000 : 'File Copy Error',
                    1001 : 'Operating System Error',
                    1002 : 'Compiler Error',
                    1003 : 'Linker Error',
                    1004 : 'File IO Error',
                    1005 : 'Unable to remove directory'
                  }
    return error_value.get(value, 'Unknown Error')
    
def name(value):
    name = str(value)
    name = name.split(' ')
    name = name[0]
    name = name.split('.')
    name = name.pop()
    name = name.split('(')
    name = name[0].replace('<', '')
    return name

