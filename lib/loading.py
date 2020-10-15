import os
import sys
import time

def simple(process, msg, cls = True):
    while process.isAlive() :
        chars = "/—\|" 
        for char in chars:
            sys.stdout.write('\r'+msg+char)
            time.sleep(.1)
            sys.stdout.flush()
    if cls: os.system("cls")
    else: sys.stdout.write("\033[B\033[F\033[K\033[A")
    return True