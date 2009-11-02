import os
import os.path

monkey_files = ['/home/test/buildit/src/main.cpp',
         '/home/test/buildit/src/classes.hpp',
         '/home/test/buildit/src/modules.h',
         '/home/test/buildit/inc/test.h'
         ]

def monkey_getcwd():
    return '/home/test/buildit/'

def monkey_exists(path):
    return path in monkey_files

def monkey_makedirs(directory):
    return True

os.getcwd = monkey_getcwd
os.path.exists = monkey_exists
os.makedirs = monkey_makedirs
