# Color printing messages 

import sys
import threading
import ctypes.windll.kernel32 as windll

if sys.platform == 'win32':
    green = 0x0002
    red = 0x0004
    magenta = 0x0005
    yellow = 0x0006

else:
    green = '\33[1;32m'
    red = '\33[1;31m'
    magenta = '\33[1;35m'
    yellow = '\33[1;33m'

print_lock = threading.Lock()

def cprint(message, color):
    print_lock.acquire()
    if sys.platform == 'win32':
        handle = windll.GetStdHandle(-11)
        windll.SetConsoleTextAttribute(handle, color | 0x0008)
        print(message),
        windll.SetConsoleTextAttribute(handle, 0x0007) # Set it back to white
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
