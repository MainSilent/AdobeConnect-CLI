import os
import sys; sys.path.insert(0, 'lib')
import urllib.request
import loading
import threading
from winreg import *
from website import Website
from termcolor import cprint 
from datetime import datetime
from schoolProgram import Program
from apscheduler.scheduler import Scheduler

# Checking network connection
while True:
	try:
		print("Checking network connection...")
		urllib.request.urlopen('https://google.com', timeout=1)
		break
	except: 
		os.system("cls")
		print("No Internet Connection.")
		input("press enter to try again: ")
		continue

# init registry
keyVal = 'Software\\AdobeConnect-CLI'
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
while user.status[0]:
	print(user.status[1])
	if user.status[0] == 401:
		nationalId = input("Enter your national id: ")
		user = Website(nationalId)
	else: input("press enter to try again: ")

	loading_process = threading.Thread(target=user.login)
	loading_process.start()
	login = loading.simple(loading_process, "Login... ")
	loading_process.join()


# Write login detail to registry
SetValueEx(key, "nationalId", 0, REG_SZ, nationalId)
CloseKey(key)

while True:
	sched = Scheduler()
	sched.start()
	# School Program
	now = datetime.now()
	program = Program()
	for lesson in program.today():
		try:
			stime = datetime.strptime(lesson['stime'],'%H:%M')
			etime = datetime.strptime(lesson['etime'],'%H:%M')
		except ValueError:
			print("Incorrect time format for: "+lesson['name'])
			continue

		if now.time() > stime.time() and now.time() < etime.time():
			print(lesson['name'], end=" | ")
			print(lesson['stime'] + " - " + lesson['etime'])
			loading_process = threading.Thread(target=user.openClass, args=[lesson['name_in_website']])
			loading_process.start()
			print(); login = loading.simple(loading_process, "Getting "+lesson['name']+" URL... ", False)
			loading_process.join()
			if user.status[0] == 404:
				cprint(" Error: Can't find "+lesson['name'], 'red')
		else:
			if stime.time() > now.time():
				datetime = now.replace(hour=stime.hour, minute=stime.minute, second=stime.second)
				sched.add_date_job(user.openClass, datetime, [lesson['name_in_website']])
			cprint(lesson['name'], 'white', end=" | ")
			print(lesson['stime'] + " - " + lesson['etime'])
	input()
	if input("Enter 'q' to quit: ") == "q": break
	os.system("cls")