#!/usr/bin/env python
# Rhymes with bake, rake, and make
# This is the "execution" script. By default it will read from a "snakefile". 
# Requires buildit to be installed.

import os
import sys

from optparse import OptionParser

from buildit.cprint import error

if __name__ == '__main__':
    parser = OptionParser(conflict_handler='resolve')
    parser.add_option('-f', '--file', dest='file_name',
                      default='snakefile', help='run from FILE_NAME')
    options, args = parser.parse_args()
    try:
        with open(options.file_name) as snake_file:
            run_string = 'from buildit import *\n{0}'.format(''.join(snake_file)) 
            run_string = '{0}\nbuildit.run()'.format(run_string)
            exec(run_string)
    except IOError:
        error('Could not open file:{0}'.format(options.file_name))
