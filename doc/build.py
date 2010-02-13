#!/usr/bin/env python
# buildit 0.2 documentation

import os
import sys
import shutil

from glob import glob

import textile

def generate_docfile(file_name):
    txt_file = file_name
    name = file_name
    file_name = file_name.split('.')
    file_name.pop()
    name = name.split('/')
    name = name.pop()
    name = name.split('.')
    name = name.pop(0)
    file_name.append('html')
    file_name = '.'.join(file_name)
    file_name = '../html/{0}'.format(file_name)
    write_dir = file_name.split('/')
    write_dir.pop()
    write_dir = '/'.join(write_dir)
    try: os.makedirs(write_dir)
    except: pass
    file = open(file_name, 'w')
    header = open('templates/header.txt')
    for line in header:
        if '<title>' in line and '</title>' in line:
            line = line.format(name)
        file.write(line)
    header.close()
    txt_file = open(txt_file)
    txt_string = ''
    for line in txt_file:
        txt_string += line
    file.write(textile.textile(txt_string))
    txt_file.close()
    footer = open('templates/footer.txt')
    for line in footer:
        file.write(line)
    footer.close()
    file.close()

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
            if 'templates' in root: continue
            file_list.append('{0}/{1}'.format(root, file))
    file_list = fix_paths(file_list)
    for file in file_list:
        if file.endswith('.txt'):
            generate_docfile(file)
    for root, dir, files in os.walk('.'):
        if 'templates' in root: continue
        shutil.copy('style.css', '../html/{0}'.format(root))
