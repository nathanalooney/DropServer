import urllib2
import requests
import json

if __name__ == "__main__":

	files = {'file': open('testfile.txt', 'rb')}
	r = requests.post('http://localhost:8000/syncfolder/send', files = files)
	print "Successful send!"
	