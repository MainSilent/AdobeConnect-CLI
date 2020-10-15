import os
import re
import sys
import time
import requests
import webbrowser
from bs4 import BeautifulSoup
from urllib.parse import unquote

class Website:
	page = ""
	status = [0, '']
	session = requests.Session()

	def __init__(self, identity):
		self.identity = identity
		self.name = "User"

	def login(self):
		url_login = 'http://vc.nik-akhtar.ir/login/index.php'

		while (True):
			try:
				# Get Token
				page = self.session.get(url_login)
				soup = BeautifulSoup(page.content, 'html.parser')
				results = soup.find(id='login')
				token = results.find_all('input')[1]['value']

				# send login request
				payload = {
					'username': self.identity,
					'password': self.identity,
					'logintoken': token
				}
				response = self.session.post(url_login, data=payload)

				if "logintoken" in response.text:
					os.system('cls')
					msg = "Login faild, try again."
					self.status = [401, msg]
					return
				else:
					self.page = BeautifulSoup(response.content, 'html.parser')
					self.name = self.page.find_all("h1")[0].text
					break
			except:
				os.system('cls')
				print("Problem with login, try again.")
				continue

	def openClass(self, lesson):
		try:
			if "logintoken" in str(self.page) or self.page == "":
				print("Session faild, try to login.")
				self.login()

			elems = self.page.find_all("div", class_="media-body")
			found = False
			# do all the redirects 😥
			for elem in elems:
				name = elem.find("h4").find("a").text
				url = elem.find("h4").find("a")["href"]
				if lesson in name:
					found = True
					response = self.session.get(url)
					soup = BeautifulSoup(response.content, 'html.parser')

					url = soup.find_all("div", class_="activityinstance")[1].find("a")["href"]
					response = self.session.get(url)
					soup = BeautifulSoup(response.content, 'html.parser')

					onclick = soup.find_all("input")[3]["onclick"]
					url = re.search("(?P<url>https?://[^\s]+)", onclick).group("url").strip("',")

					# Adobe Connect URL
					response = self.session.get(url)
					soup = BeautifulSoup(response.content, 'html.parser')
					script = soup.find_all("script")[5]
					script_regex = re.search("https?[^\s]+;", str(script)).group().strip("';")+";"
					adobe_url = "connectpro:" + script_regex

					webbrowser.open(unquote(adobe_url))
					break

			if not found: 
				print("Can't find the lesson")
				return False

			return True

		except Exception as e:
			os.system('cls')
			print("Error: " + e)