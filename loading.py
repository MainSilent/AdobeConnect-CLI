import os
import sys
import time

def simple(process, msg):
    while process.isAlive() :
        chars = "/—\|" 
        for char in chars:
            sys.stdout.write('\r'+msg+char)
            time.sleep(.1)
            sys.stdout.flush()
    os.system("cls")
    return True