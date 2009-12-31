#!/usr/bin/env python
# buildit 0.2 documentation

import os
import sys
import shutil

import markdown2

def generate_docfile(file_name):
    return file_name

def fix_paths(file_list):
    if sys.platform == 'win32':
        file_list = [file_name.replace('\\', '/') for file_name in file_list]
        file_list.sort()
    return file_list

if __name__ == '__main__':
    try:
        os.makedirs('../html')
    except OSError:
        pass
    file_list = []
    for root, dir, files in os.walk('.'):
        for file in files:
            file_list.append('{0}/{1}'.format(root, file))
    file_list = fix_paths(file_list)
    for file in file_list:
        if file.endswith('.txt'):
            file = generate_docfile(file)
        try:
            shutil.copyfile(file, '../html')
        except:
            pass
            
