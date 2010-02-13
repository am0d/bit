# Color printing messages 

import sys
import threading
if sys.platform == 'win32':
    import ctypes
    magenta = 0x0005
    yellow = 0x0006
    green = 0x0002
    red = 0x0004
    
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    short = ctypes.c_short
    ushort = ctypes.c_ushort
    
    # Well it's not *all* bad :V
    class Coord(ctypes.Structure):
        _fields_ =[('X', short), ('Y', short)]
    class SmallRect(ctypes.Structure):
        _fields_ = [('Left', short), ('Top', short), 
                    ('Right', short), ('Bottom', short)]
    class ConsoleScreenBufferInfo(ctypes.Structure):
        _fields_ = [('dwSize', Coord), ('dwCursorPosition', Coord),
                    ('wAttributes', ushort), ('srWindow', SmallRect), 
                    ('dwMaximumWindowSize', Coord)]

    csbi = ConsoleScreenBufferInfo()
    # Keep in line with the Windows API. Sort of >_>
    def get_console_text_attribute(handle):
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, 
            ctypes.byref(csbi))
        return csbi.wAttributes

    default_colors = get_console_text_attribute(handle)
    background = default_colors & 0x0070
    primary_color = default_colors & 0x0007

else:
    magenta = '\33[1;35m'
    yellow = '\33[1;33m'
    green = '\33[1;32m'
    red = '\33[1;31m'
    
print_lock = threading.Lock()

def cprint(message, color):
    print_lock.acquire()
    if sys.platform == 'win32':
        handle = ctypes.windll.kernel32.GetStdHandle(-11)
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 
            color | 0x0008 | background)
        print(message),
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 
            primary_color | 0x0008 | background)
        print('')
    else:
        print('{0}{1}\33[0m'.format(color, message))
    print_lock.release()

def info(message):
    cprint(message, green)
    
def warning(message):
    cprint(message, yellow)

def error(message):
    cprint(message, red)
    
def command(message):
    cprint(message, magenta)
