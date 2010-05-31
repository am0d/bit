# Color Printing Module

import sys
import threading

from bit.instance import bit

if sys.platform == 'win32':
    import ctypes
    fcolor = { 'blue'   : 0x0001,
               'green'  : 0x0002,
               'cyan'   : 0x0003,
               'red'    : 0x0004,
               'magenta': 0x0005, 
               'yellow' : 0x0006,
               'white'  : 0x0007,
             }

    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    short = ctypes.c_short
    ushort = ctypes.c_ushort

    class Coord(ctypes.Structure):
        _fields_ = [('X', short), ('Y', short)]

    class SmallRect(ctypes.Structure):
        _fields_ = [('Left', short), ('Top', short),
                    ('Right', short), ('Bottom', short)]

    class ConsoleScreenBufferInfo(ctypes.Structure):
        _fields_ = [('dwSize', Coord), ('dwCursorPosition', Coord),
                    ('wAttributes', ushort), ('srWindow', SmallRect),
                    ('dwMaximumWindowSize', Coord)]

        @property
        def attributes(self):     
            return self.wAttributes

    csbi = ConsoleScreenBufferInfo()

    def get_console_text_attribute(handle):
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle,
                ctypes.byref(csbi))
        return csbi.attributes
    set_console_text_attribute = ctypes.windll.kernel32.SetConsoleTextAttribute

    default_colors = get_console_text_attribute(handle)
    background = default_colors & 0x0070
    primary_color = default_colors & 0x0007

else: # Assume the terminal supports ascii colors
    fcolor = { 'red'    : '\33[1;31m',
               'green'  : '\33[1;32m',
               'yellow' : '\33[1;33m',
               'blue'   : '\33[1;34m',
               'magenta': '\33[1;35m',
               'cyan'   : '\33[1;36m',
               'white'  : '\33[1;37m',
             }

print_lock = threading.Lock()

def string_color_print(message, color):
    print_lock.acquire()
    if bit.options.no_color:
        print(message)
        print_lock.release()
        return
    if sys.platform == 'win32':
        set_console_text_attribute(handle, fcolor[color] | 0x0008 | background)
        print(message),
        set_console_text_attribute(handle, primary_color | 0x0008 | background)
        print('')
    else:
        print('{0}{1}\33[0m'.format(fcolor[color], message))
    print_lock.release()

def string_char_print(char, color):
    print_lock.acquire()
    if bit.options.no_color:
        sys.stdout.write(char)
        return
    if sys.platform == 'win32':
        set_console_text_attribute(handle, fcolor[color] | 0x0008 | background)
        sys.stdout.write(char)
        set_console_text_attribute(handle, primary_color | 0x0008 | background)
    else:
        print('{0}{1}\33[0m'.format(fcolor[color], char))
    print_lock.release()

def success(message):
    string_color_print(message, 'green')

def warning(message):
    string_color_print(message, 'yellow')

def error(message):
    string_color_print(message, 'red')

def command(message):
    string_color_print(message, 'magenta')

def info(message):
    string_color_print(message, 'cyan')
