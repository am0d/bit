import sys
from buildit import *

if sys.platform == 'win32':
    bit = MinGW('bit')
else:
    bit = Unix('bit')
bit.add('bit.c')
if sys.platform == 'win32':
    bit.add_include_directory('C:/Python26/include')
    bit.add_library_directory('C:/Python26/libs')
bit.add_library('python26')
bit.add_flag('-Wall', '-pedantic', '-ansi', '-Warray-bounds', '-Wextra', '-Wclobbered', '-Wconversion')
bit.add_flag('-O3')
bit.add_link_flag('-s')
bit.C99
bit.build_directory = '.'
try:
    bit.run()
except:
    bit.pause()
