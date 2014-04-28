from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from pathlib import Path
import shutil
import os
import requests
import pickle
from sendfile import sendfile







# Create your views here.
def index(request):
	return HttpResponse("<h1> Index </h1>")




def fileCreate(request):

	if request.method=='POST':
		print "Request Received: Create File"
		if 'file' in request.FILES:
			print "Type: File"


			fd = request.FILES['file']
			path = Path(request.FILES['path'].read())
			time = request.FILES['time'].read()
			idNum = request.FILES['ID'].read()
			user = request.FILES['username'].read()


			abspath = Path('folders/' + str(user) + '/' + str(path))

			print os.path.exists('folders/' + str(user))
			if not os.path.exists('folders/' + str(user)):
				os.mkdir('folders/' + str(user))


			print str(abspath)

			fl = open(str(abspath), 'wb')
			data = fd.read()
			fl.write(data)
			fl.close

			pickFile = pickle.load(open('fileIndexes/' + user + '.pkl', 'rb'))
			print 'Here i am'
			pickFile['fileList'].append({'path': str(path), 'ID': idNum, 'time': time})
			pickle.dump(pickFile, open('fileIndexes/' + user + '.pkl', 'wb'))

	return HttpResponse("Success")






def dirCreate(request):
	if request.method=='POST':
			print "Request Received: Create Directory"
			path = Path(request.FILES['path'].read())
			user = request.FILES['username'].read()
			idNum = request.FILES['ID'].read()


			abspath = Path('folders/' + user + '/' + str(path))
			print "Path: " + str(abspath)
			try:
				os.makedirs(str(abspath))
			except:
				print "Invalid path"
				return HttpResponse("Invalid Path")


			pickFile = pickle.load(open('fileIndexes/' + user + '.pkl', 'rb'))

			pickFile['dirList'].append({'path': str(path), 'ID': int(idNum)})
			print str(pickFile)
			pickle.dump(pickFile, open('fileIndexes/' + user + '.pkl', 'wb'))


	return HttpResponse("Success")


def fileDelete(request):
	if request.method=='POST':
		print "Received request: Delete File"

		user = request.FILES['username'].read()
		idNum = request.FILES['ID'].read()

		pickFile = pickle.load(open('fileIndexes/' + str(user) + '.pkl', 'rb'))


		path = ''
		for files in list(pickFile['fileList']):
			print 'Iter works'
			if int(files['ID']) == int(idNum):
				path = files['path']
				pickFile['fileList'].remove(files)


		pickle.dump(pickFile, open('fileIndexes/' + user + '.pkl', 'wb'))
	
		abspath = 'folders/' + user + '/' + str(path)
		os.remove('folders/' + user + '/' + str(path))


	return HttpResponse('Success')

def dirDelete(request):
	if request.method=='POST':
		print "Received Request: Remove Directory"

		user = request.FILES['username'].read()
		idNum = request.FILES['ID'].read()
		print "Read"
		pickFile = pickle.load(open('fileIndexes/' + str(user) + '.pkl', 'rb'))
		print "Pickle"

		path = ''
		for files in list(pickFile['dirList']):
			print 'Iter works'
			if int(files['ID']) == int(idNum):
				print "if works"
				path = files['path']
				pickFile['dirList'].remove(files)


		pickle.dump(pickFile, open('fileIndexes/' + str(user) + '.pkl', 'wb'))
		print "Dump works"
		abspath = 'folders/' + str(user) + '/' + str(path)
		print abspath

		shutil.rmtree(abspath)
	return HttpResponse('Success')







def move(request):
	if request.method=='POST':
		print "Request Received: Move"

		user = request.FILES['user'].read()
		src = request.FILES['source'].read()
		dest = request.FILES['dest'].read()

		print "Reads succesful"

		abssrc = Path('folders/' + user + '/' + src)
		absdest = Path('folders/' + user + '/' + dest)

		print 'Source: ' + str(abssrc)
		print 'Dest: ' + str(absdest)

		shutil.move(str(abssrc), str(absdest))

		return HttpResponse('<p> Move <p>')






def update(request):
	if request.method=='POST':
		print "Request Received: Update"
		if 'file' in request.FILES:
			fd = request.FILES['file']
			idNum = int(request.FILES['ID'].read())
			path = Path(request.FILES['path'].read())
			user = request.FILES['username'].read()
			time = request.FILES['time'].read()
			abspath = Path('folders/' + str(user) + '/' + str(path))
			pickFile = pickle.load(open('fileIndexes/' + str(user) + '.pkl', 'rb'))
			
			print str(abspath)

			for files in pickFile['fileList']:
				if files['ID']== int(idNum):
					print "Attempting delete"
					os.remove('folders/' + str(user)+ '/' + str(files['path']))
					print "Delete Succesful"



			fl = open(str(abspath), 'wb')
			data = fd.read()
			fl.write(data)
			fl.close
			print "Update Succesful"



			
			insertDict = {'path': str(path), 'serverTime': 'updatedTime'}


			for files in pickFile['fileList']:
				if int(files['ID']) == int(idNum):
					files['serverTime'] = time
					files['path'] = str(path)

			pickle.dump(pickFile, open('fileIndexes/' + str(user) + '.pkl', 'wb'))
			print "Index Updated"


	return HttpResponse("Success")




def pull(request):
	user = request.FILES['username'].read()
	idNum = request.FILES['ID'].read()
	pickFile = pickle.load(open('fileIndexes/' + str(user) + '.pkl', 'rb'))
	path = ''
	print "reads work"

	for files in list(pickFile['fileList']):
		print 'Iter works'
		if int(files['ID']) == int(idNum):
			print "if works"
			path = files['path']

	print path

	r = open('folders/' + str(user) + '/' + str(path), 'rb')
	print 'folders/' + user + '/' + path
	print os.path.exists('folders/' + str(user) + '/' + str(path))

	return HttpResponse(r)

def getServerIndex(request):
	print "Request Received"
	user = request.FILES['username'].read()
	fil = open('fileIndexes/' + user + '.pkl', 'rb')
	print os.path.exists('fileIndexes/' + user + '.pkl')
	#return sendfile(request, 'fileIndexes/' + user + '.pkl')
	#index = pickle.load(r)
	#print index
	#print "File opened"
	#print r
	return HttpResponse(fil)


def login(request):
	return StreamingHttpResponse("<h1> Login </h1>")





