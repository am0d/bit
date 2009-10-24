import os
import os.path

def monkey_getcwd():
    return '/home/test/buildit/'

def monkey_exists(path):
    files = ['/home/test/buildit/src/main.cpp',
             '/home/test/buildit/src/classes.hpp',
             '/home/test/buildit/src/modules.h',
             '/home/test/buildit/inc/test.h'
             ]
    return path in files

os.getcwd = monkey_getcwd
os.path.exists = monkey_exists
