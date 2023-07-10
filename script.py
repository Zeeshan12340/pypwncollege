#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# base script taken from https://github.com/p0dalirius/ctfd-parser
# Author             : Zeeshan1234

import argparse
import json
import requests
import re
import os
from getpass import getpass
from bs4 import BeautifulSoup
from pwn import log

class CTFdParser(object):

	def __init__(self, target, login, password):
		super(CTFdParser, self).__init__()
		self.target = target
		self.challenges = {}
		self.credentials = {
			'user': login,
			'password': password
		}
		self.session = requests.Session()
		self.dojos = {}
		self.csrf = ""

	def login(self):
		p = log.progress("Trying to log in...")
		r = self.session.get(self.target + '/login')
		matched = re.search(
			b"""('csrfNonce':[ \t]+"([a-f0-9A-F]+))""", r.content)
		nonce = ""
		if matched is not None:
			nonce = matched.groups()[1]
		
		r = self.session.post(
			self.target + '/login',
			data={
				'name': self.credentials['user'],
				'password': self.credentials['password'],
				'_submit': 'Submit',
				'nonce': nonce.decode('UTF-8')
			}
		)
		p.success("Logged in Successfully!")

		r = self.session.get(self.target + '/')
		matched = re.search(
			b"""('csrfNonce':[ \t]+"([a-f0-9A-F]+))""", r.content)
		nonce = ""
		if matched is not None:
			nonce = matched.groups()[1]
		self.csrf = nonce.decode('UTF-8')

		return 'Your username or password is incorrect' not in r.text

	def get_dojos(self, threads=8):
		r = self.session.get(self.target + "/dojos")

		if r.status_code == 200:
			soup = BeautifulSoup(r.content, 'html.parser')

			data = "\n----- Courses -----\n"
			count = 1
			for i in range(1, 20, 2):
				try:
					data += f"{count}. "
					data += soup.find_all("div", class_="container")[2].contents[3].contents[i].h4.contents[0]
					self.dojos[soup.find_all("div", class_="container")[2].contents[3].contents[i].attrs['href']] = []
					data += "\n"
				except IndexError:
					break
				count += 1
			data += "\n-----------------\n"

			data += "\n----- Topics -----\n"
			for i in range(1, 20, 2):
				try:
					data += f"{count}. "
					data += soup.find_all("div", class_="container")[2].contents[9].contents[i].h4.contents[0]
					self.dojos[soup.find_all("div", class_="container")[2].contents[9].contents[i].attrs['href']] = []
					data += "\n"
				except IndexError:
					break
				count += 1
			data += "\n-----------------\n"

			data += "\n----- More -----\n"
			for i in range(1, 20, 2):
				try:
					data += f"{count}. "
					data += soup.find_all("div", class_="container")[2].contents[15].contents[i].h4.contents[0]
					self.dojos[soup.find_all("div", class_="container")[2].contents[15].contents[i].attrs['href']] = []
					data += "\n"
				except (IndexError, AttributeError):
					break
				count += 1
			data += "\n-----------------\n"

			return data
		else:
			return None

	def get_modules(self, index):
		dojo = list(self.dojos)[index]
		r = self.session.get(self.target + dojo)
		if r.status_code == 200:
			soup = BeautifulSoup(r.content, 'html.parser')
			data = f"\n----- Modules in {dojo.strip('/dojo/')} -----\n"
			count = 1
			for i in range(1, 20, 2):
				try:
					data += f"{count}. "
					data += soup.find_all("ul")[2].contents[i].h4.contents[0]
					self.dojos[dojo].append(soup.find_all("ul")[2].contents[i].attrs['href'])
					data += "\n"
				except IndexError:
					break
				count += 1
			data += "\n-----------------\n"

			return data
		else:
			return None


	def get_challenges(self, dojo_index, module_index):
		dojo = list(self.dojos)[dojo_index]
		module = self.dojos[dojo][module_index]
		r = self.session.get(self.target + module)
		if r.status_code == 200:
			soup = BeautifulSoup(r.content, 'html.parser')
			data = f"\n----- Challenges in {module.split('/')[2]} -----\n"
			count = 1
			for i in range(0, 1000, 3):
				try:
					data += f"{count}. "
					data += soup.find_all("span", class_="d-sm-block d-md-block d-lg-block")[i].contents[2].strip()
					data += "\n"
				except IndexError:
					break
				count += 1
			data += "\n-----------------\n"

			return data
		else:
			return None

	def start_challenge(self, dojo_index, module_index, level, practice):
		dojo = list(self.dojos)[dojo_index]
		module = (self.dojos[dojo][module_index]).split('/')[2]
		challenge = f"level-{level.replace('.','-').strip()}"

		url = target + "/pwncollege_api/v1/docker"
		headers = {"Csrf-Token": self.csrf }
		data = {"challenge": challenge,
				"dojo": dojo.strip('/dojo/'),
				"module": module,
				"practice": practice
				}
		p = log.progress("Starting Challenge... ")
		r = self.session.post(url, headers=headers, json=data)
		data = json.loads(r.text)

		if 'success' not in data:
			p.failure(data['message'])
		elif data['success']:
			p.success("Started!")
		else:
			p.failure(data['error'])

	def show_scoreboard(self, dojo_index, module_index):
		dojo = list(self.dojos)[dojo_index]
		if module_index > 0:
			module = (self.dojos[dojo][module_index]).split('/')[2]
			dojo = dojo.strip('/dojo/')
			url = self.target + f"/pwncollege_api/v1/scoreboard/{dojo}/{module}/0/1"
		else:
			module = ''
			dojo = dojo.strip('/dojo/')
			url = self.target + f"/pwncollege_api/v1/scoreboard/{dojo}/_/0/1"

		p = log.progress("fetching scoreboard data...")
		r = self.session.get(url)
		p.success("fetched!")
		resp = json.loads(r.text)

		data = f"\n----- scoreboard {dojo + ' ' + module}-----\n"
		for i in range(len(resp['standings'])):
			data += f"{i+1}. "
			data += resp['standings'][i]['name']
			if "white" in resp['standings'][i]['belt']:
				data += " - white belt "
			elif "yellow" in resp['standings'][i]['belt']:
				data += " - yellow belt "
			else:
				data += " - blue belt "

			data += f"{resp['standings'][i]['solves']}/{resp['standings'][0]['solves']}\n"
		data += "--------------------------------------------\n"

		return data
		


def header():
	print(r"""                                                                                                
,------,--.   ,--,------.,--.   ,--,--.  ,--.,-----.,-----.,--.  ,--.  ,------.,----.  ,------. 
|  .--. \  `.'  /|  .--. |  |   |  |  ,'.|  '  .--.'  .-.  |  |  |  |  |  .---'  .-./  |  .---' 
|  '--' |'.    / |  '--' |  |.'.|  |  |' '  |  |   |  | |  |  |  |  |  |  `--,|  | .---|  `--,  
|  | --'   |  |  |  | --'|   ,'.   |  | `   '  '--''  '-'  |  '--|  '--|  `---'  '--'  |  `---. 
`--'       `--'  `--'    '--'   '--`--'  `--'`-----'`-----'`-----`-----`------'`------'`------' 
																								""")
	return

def parseArgs():
	header()
	parser = argparse.ArgumentParser(description="PyPwncollege")
	parser.add_argument("-u", "--user", required=True, help="Username/email to login to pwncollege")
	parser.add_argument("-p", "--password", required=False, help="Password to login to pwncollege (default: interactive)")
	return parser.parse_args()

def menu():
	print("You can do the following: ")
	print("--------------------------------")
	print("1. list dojos/modules/challenges")
	print("2. start challenge in a dojo")
	print("3. list scoreboard for dojo/module")
	print("4. exit")
	print("--------------------------------")
	print("type 'back' at any prompt to go back to main menu")
	return input("> ")

if __name__ == '__main__':
	args = parseArgs()

	target = "https://pwn.college"

	if args.password is None:
		args.password = getpass("Password: ")

	cp = CTFdParser(target, args.user, args.password)
	if cp.login():
		while True:
			choice = int(menu())
			match choice:
				case 1:
					print(cp.get_dojos())

					data = input("Which dojo do you want to see?(index)\n> ")
					if 'back' not in data:
						dojo_index = int(data)
					else:
						continue
					print(cp.get_modules(dojo_index-1))

					data = input("Which module do you want to see?(index)\n> ")
					if 'back' not in data:
						module_index = int(data)
					else:
						continue
					print(cp.get_challenges(dojo_index-1, module_index-1))

				case 2:
					print("Select Dojo:")
					print("------------")
					print(cp.get_dojos())
					data = input("> ")
					if 'back' not in data:
						dojo_index = int(data)
					else:
						continue

					print("Select Module:")
					print("------------")
					print(cp.get_modules(dojo_index-1))
					data = input("> ")
					if 'back' not in data:
						module_index = int(data)
					else:
						continue

					print("Select Level: \n(specify dot level if present, e.g '1.0')")
					print(cp.get_challenges(dojo_index-1, module_index-1))
					data = input("> ")
					if 'back' not in data:
						level = data
					else:
						continue

					practice = input("Start in practice mode?(default: practice)(n for normal)\n> ")
					if practice == 'n':
						practice = False
					elif practice == 'back':
						continue
					else:
						practice = True
					cp.start_challenge(dojo_index-1, module_index-1, level, practice)

				case 3:
					print("Select Dojo:")
					print("------------")
					print(cp.get_dojos())
					data = input("> ")
					if 'back' not in data:
						dojo_index = int(data)
					else:
						continue

					print("Do you want to see a module's scoreboard?(y/n)")
					choice = input("> ")
					print(choice)
					if 'y' in choice:
						print("Select Module:")
						print("------------")
						print(cp.get_modules(dojo_index-1))
						data = input("> ")
						if 'back' not in data:
							module_index = int(data)
						else:
							continue
					else:
						module_index = 0

					print(cp.show_scoreboard(dojo_index-1, module_index-1))

				case 4:
					print("Exiting....")
					exit(0)

				case _:
					print("invalid choice")

	else:
		print("[-] Login failed")