import shutil
import os
import requests
import pickle
from pathlib import Path
import json
import time
import sys
import client
import sync




if __name__ == '__main__':



	while True:
		choice = str(raw_input("Would you like to register a new account? (y/n): "))
		user = str(raw_input("Username: "))
		pword = str(raw_input("Password: "))
		files = {"username": user, "password": pword}
		loginCheck = False

		if choice=="y":

			r = requests.post("http://localhost:8000/syncfolder/setup", files=files)
			resp = r.text
			if resp == "Success":
				print "Account Created"
				loginCheck = True
			elif resp == "Failure: Username Exists":
				print resp

			folder = str(raw_input("What folder would you like to watch? (Enter full path): "))






		elif choice=="n":

			r = requests.post("http://localhost:8000/syncfolder/login", files=files)

			if r.text=="Success":
				print "Login Successful"
				loginCheck=True

			else:
				print "Login Failure"

		if loginCheck == True:
			break
		else:
			continue






	