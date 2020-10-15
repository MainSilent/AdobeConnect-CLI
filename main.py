import sys
import loading
import threading
from winreg import *
from website import Website

# init registry
keyVal = 'Software\\Goshad'
try:
    key = OpenKey(HKEY_CURRENT_USER, keyVal, 0, KEY_ALL_ACCESS)
except:
    key = CreateKey(HKEY_CURRENT_USER, keyVal)

# Login
try:
	nationalId = QueryValueEx(key, "nationalId")[0]
except:
	nationalId = input("Enter your national id: ")

user = Website(nationalId)

loading_process = threading.Thread(target=user.login)
loading_process.start()
login = loading.simple(loading_process, "Login... ")
loading_process.join()

# try Login again if failed
while user.status[0] == 401:
	print(user.status[1])
	nationalId = input("Enter your national id: ")
	user = Website(nationalId)

	loading_process = threading.Thread(target=user.login)
	loading_process.start()
	login = loading.simple(loading_process, "Login... ")
	loading_process.join()

# Write login detail to registry
SetValueEx(key, "nationalId", 0, REG_SZ, nationalId)
CloseKey(key)

# loading_process = threading.Thread(target=user.openClass, args=("شیمی",))
# loading_process.start()
# login = loading.simple(loading_process, "Getting Lesson URL... ")
# loading_process.join()