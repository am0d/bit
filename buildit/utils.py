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

def archive(directory, name='archive', ark='bz2'):
    if not ark == 'zip':
        ark_type = {'bz2': 'w:bz2', 'gz': 'w:gz'}
        ark_type = ark_type.get(ark, 'bz2')
        ark_ext = '.tar.{0}'.format(ark_type)
    else:
        ark_ext = '.{0}'.format(ark)
    ark_name = name
    if ark == 'zip':
        ark_file = zipfile.ZipFile('{0}{1}'.format(ark_name, ark_ext), 'w')
        ark_file.write(directory)
    else:
        ark_file = tarfile.open('{0}{1}'.format())
        ark_file.add(directory)
    ark_file.close()

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
    if system_type == 'windows':
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

def system_type():
    systems = {'win32': 'windows', 'cygwin': 'windows',
               'linux': 'linux', 'linux2': 'linux',
               'darwin': 'apple'}
    return systems.get(sys.platform, 'generic')
    
def flatten(list_name, containers=(list, tuple)):
    if isinstance(list_name, containers):
        if len(list_name) < 1:
            return []
        else:
            return reduce(lambda x, y : x + y, map(flatten, list_name))
    else:
        return [list_name]

def fix_strings(file_list):
    if isinstance(file_list, list) or isinstance(file_list, tuple):
        if system_type() == 'windows':
            for file_name in file_list:
                file_list.remove(file_name)
                file_name = os.path.normpath(file_name)
                file_list.append(file_name)
                file_list.sort()
        else:
            file_list.sort()
    return file_list

def format_options(option_list, option=''):
    string = ''
    option_list = flatten(option_list)
    for item in option_list:
        string += ' {0}{1}'.format(option , item)
    return string
    
    
def lookup_error(value):
    error_value = {
                    1000 : 'File Copy Error',
                    1001 : 'Operating System Error',
                    1002 : 'Compiler Error',
                    1003 : 'Linker Error'
                  }
    return error_value.get(value, 'Unknown Error')
    
