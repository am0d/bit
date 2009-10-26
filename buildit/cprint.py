# Color printing messages 

import sys
import threading
if sys.platform == 'win32':
    import ctypes
    magenta = 0x0005
    yellow = 0x0006
    green = 0x0002
    red = 0x0004
    
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
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color | 0x0008)
        print(message),
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, 0x0007)
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
