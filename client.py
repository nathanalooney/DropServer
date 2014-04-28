import shutil
import os
import requests
import pickle
from pathlib import Path
import json
import time
import sys
import client




if __name__ == '__main__':

	choice = str(raw_input("Would you like to register a new account? (y/n): "))



	user = str(raw_input("Username: "))
	pword = str(raw_input("Password: "))
	files = {"username": user, "password": pword}

	if choice=="y":

		requests.post("http://localhost:8000/setup", file=files)

	elif choice=="n":

		requests.post("http://localhost:8000/setup")



	