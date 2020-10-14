import os
import sys
import time
import requests
from bs4 import BeautifulSoup

class Website:
	def __init__(self, identity):
		self.identity = identity
		self.name = "User"

	def login(self):
		url_login = 'http://vc.nik-akhtar.ir/login/index.php'

		while (True):
			try:
				# Get Token
				page = requests.get(url_login)
				soup = BeautifulSoup(page.content, 'html.parser')
				results = soup.find(id='login')
				token = results.find_all('input')[1]['value']
				self.session = 'MoodleSession='+page.cookies["MoodleSession"]

				# send login request
				payload = {
					'username': self.identity,
					'password': self.identity,
					'logintoken': token
				}
				headers = {'Cookie': self.session}
				response = requests.post(url_login, data=payload, headers=headers)

				if "logintoken" in response.text:
					os.system('cls')
					print("\nLogin faild, try again.")
					continue
				else:
					self.page = BeautifulSoup(response.content, 'html.parser')
					self.name = self.page.find_all("h1")[0].text
					break
			except:
				os.system('cls')
				print("\nProblem with login, try again.")
				continue

	def openClass(self, lesson = "دینی"):
		elems = self.page.find_all("div", class_="media-body")
		for elem in elems:
			name = elem.find("h4").find("a").text
			url = elem.find("h4").find("a")["href"]
			if lesson in name:
				print(url)