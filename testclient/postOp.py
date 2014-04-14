import urllib2
import requests
import json
from pathlib import *

if __name__ == "__main__":


	username = 'nal3vm'
	directory = '/textfiles'
	files = {'file': open('testfile.txt', 'rb'), 'user': username, 'path': directory}

	r = requests.post('http://localhost:8000/syncfolder/send', files = files)

	print "Successful send!"
	print r.text
	