import sys
import threading
import loading
from website import Website

user = Website("2981485792")

loading_process = threading.Thread(target=user.login)
loading_process.start()
login = loading.simple(loading_process, "Login... ")
loading_process.join()

loading_process = threading.Thread(target=user.openClass, args=("شیمی",))
loading_process.start()
login = loading.simple(loading_process, "Getting Lesson URL... ")
loading_process.join()