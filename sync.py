__author__ = 'Kevin'

#TODO fix file paths - all in client absolute right now
# figure out exactly how to do the savepath
# X connection to sever/get serverIndex
# 	get real server running on other IP
# X send all posts to server from queue
#	X with this make sure on pulls to change local time on client index and resave
# make sure lists are being passed by reference and keeping value


import pickle
import os
import json
import time
import requests
import sys

def getSystemDir(path):
	direct = []
    	fil = []
    	for root, dirs, files in os.walk(path):
        	if dirs not in direct:
            		for d in dirs:
                		dir1 = root + "/" + d
				d = {'path': dir1}
                		direct.append(d)
        	if files not in fil:
            		for f in files:
                		pth = root+ "/" + f
                		statbuf = os.stat(pth)
                		t = statbuf.st_mtime
                		f1 = {'path':pth, 'modTime':t}
                		fil.append(f1)
	print fil
	print '============================'
	return {'dirs': direct, 'files': fil}

def pumpIndexTest(path, username, sysDir):
	direct = os.getcwd
	f = {'username': 'kevin', 'fileList': [], 'dirList':[]}
	idN = 1
	for d in sysD['dirs']:
		f['dirList'].append({'path': d['path'], 'ID':idN})
		idN = idN + 1
	for fil in sysD['files']:
		f['fileList'].append({'path': fil['path'], 'ID':idN, 'localTime': fil['modTime'], 'serverTime': fil['modTime']})
		idN = idN + 1

	savData = open(path+str(username)+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f

def pumpServerIndexTest(path, username, sysDir):
	#r = open('fileIndexes/' + user + '.pkl', 'rb')

	f = {'username': 'kevin', 'fileList': [], 'dirList':[]}
	#print f
	idN = 1
	#for d in sysDir['dirs']:
		#f['dirList'].append({'path': d['path'], 'ID':idN})
		#idN = idN + 1
	#for fil in sysDir['files']:
		#f['fileList'].append({'path': fil['path'], 'ID':idN, 'time': fil['modTime']})
		#idN = idN + 1

	savData = open(path+str(username)+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f


def getClientIndex(username, savePath):
	try: 
		print savePath
		print (str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
		file2 = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
	except IOError:
    		direct = os.getcwd
		fi = {'username':username, 'fileList': [], 'dirList': []}
		print (str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
    		savData = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
    		pickle.dump(fi, savData)
    		savData.close()
		file2 = open(savePath+str(username)+'.pkl', 'r+b')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex


def saveClientIndex(clientIndex, username, savePath):
	savData = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'wb')
    	pickle.dump(clientIndex, savData)
    	savData.close()
		
    	
def createDeleteList(clientIndex):
	fileDeleteList = []
	dirDeleteList = []
	for d in clientIndex['dirList']:
		if not os.path.exists(d['path']):
			print 'Delete Directory:'
			print d['path']
			dirDeleteList.append(d['ID'])
			clientIndex['dirList'].remove(d)
	for f in clientIndex['fileList']:
		if not os.path.exists(str(f['path'])):
			print 'Delete File:'
			print f['path']
			fileDeleteList.append(f['ID'])
			clientIndex['fileList'].remove(f)
	return {'fileDeleteList': fileDeleteList, 'dirDeleteList': dirDeleteList}

def getServerIndex(username, savePath):
	msg = {'username': username}
	r = requests.post('http://localhost:8000/syncfolder/getServerIndex', files = msg)
	#print r
	with open(savePath+str(username)+'Server'+'.pkl', 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
	#fil = open (savePath+str(username)+'Server'+'.pkl', 'wb')
	#fil.write(r['data'])
	#fil.close()
	serverFile = open(savePath+str(username)+'Server'+'.pkl', 'rb')
    	index = pickle.load(serverFile)
    	serverFile.close()
	os.remove(savePath+str(username)+'Server'+'.pkl')
	for d in index['dirList']:
		temp = d['ID']
		d['ID'] = str(temp)
	#os.remove(savePath+str(username)+'Server'+'.pkl')
	return index

def systemClientCompare(clientIndex, systemDict):
	dcreatelist = []
	fcreatelist = []
	updatelist = []
	for dirs in systemDict['dirs']:
		ff = next((item for item in clientIndex['dirList'] if item['path'] == dirs['path']),None)
		if ff is None:
			#print 'directory not found: ' + str(dirs['path'])
			dcreatelist.append({'path': dirs['path']})
	for fils in systemDict['files']:
		ff = next((item for item in clientIndex['fileList'] if item['path'] == fils['path']),None)

		print ff
		if ff is None:
			#print 'file not found: ' + str(fils['path'])
			fcreatelist.append({'path':fils['path'], 'time':fils['modTime']})
		else:
			#print 'this is filefound: ' + str(ff)
			if ff['localTime'] < float(fils['modTime']):
				ff['localTime'] = float(fils['modTime'])
				updatelist.append({'ID': ff['ID'], 'time': ff['localTime'], 'path': ff['path']})
	return {'dcreatelist': dcreatelist, 'fcreatelist': fcreatelist, 'updatelist': updatelist}

def clientServerCompare(clientIndex, serverIndex, fileDeleteList, dirDeleteList, updatelist, dcreatelist, fcreatelist, path, savePath, username):
	largeID = 0
	clientPullList = []
	for d in serverIndex['dirList']:
		if int(d['ID']) > largeID:
			largeID = int(d['ID'])
		dd = next((item for item in clientIndex['dirList'] if item['ID'] == d['ID']),None)
		if dd is None:
			if d['ID'] not in dirDeleteList:
				#create the directory here, dont actually need to pull it
				print path
				print d['path']
				if not os.path.exists(str(path) + '/' + str(d['path']).lstrip('/')):
					os.mkdir(str(path) + '/' + str(d['path']).lstrip('/'))
					clientIndex['dirList'].append({'path':d['path'], 'ID':d['ID']})
	for f in serverIndex['fileList']:
		if f['ID'] > largeID:
			largeID = f['ID']
		ff = next((item for item in clientIndex['fileList'] if int(item['ID']) == int(f['ID'])),None)
		if ff is None:
			if f['ID'] not in fileDeleteList:
				#print '-----------------------------------------------'
				#print f
				#print f
				clientIndex['fileList'].append({'path':str(path)+'/'+str(f['path']).lstrip('/'), 'ID':f['ID'], 'serverTime':f['time'], 'localTime':f['time']})
				clientPullList.append(f['ID'])
		else:
			#print 'FF -------------'
			#print ff
			if f['time'] > ff['serverTime']:
				clientPullList.append(f['ID'])
				ff['serverTime'] = f['time'] #when pull down update the local time then
				if f['ID'] in updatelist:
					updatelist.remove(f['ID'])
	#delete 
	for f in clientIndex['fileList']:	
		ff = next((item for item in serverIndex['fileList'] if item['ID'] == f['ID']),None)
		if ff is None:
			os.remove(f['path'])
			clientIndex['fileList'].remove(f)
	for d in clientIndex['dirList']:	
		dd = next((item for item in serverIndex['dirList'] if item['ID'] == d['ID']),None)
		if dd is None:
			try:
				os.rmdir(d['path'])
				clientIndex['dirList'].remove(d)
			except OSError:
				print 'dont delete that folder'
	for d in dcreatelist:
		d['ID'] = str(int(largeID) + 1)
		clientIndex['dirList'].append({'ID':d['ID'], 'path': d['path']})
		largeID = int(largeID) + 1
	for f in fcreatelist:
		f['ID'] = str(int(largeID) + 1)
		clientIndex['fileList'].append({'ID':f['ID'], 'path': f['path'], 'localTime': f['time'], 'serverTime':f['time']})
		#print 'CLIENT CREATING      DOIDODOIDIODIO'
		#print clientIndex
		largeID = int(largeID) +1
	
	saveClientIndex(clientIndex, username, savePath)

	return clientPullList


def sendPosts(clientIndex, clientPullList, fileDeleteList, dirDeleteList, updatelist, dcreatelist, fcreatelist, username, path):
	q = []
	for p in clientPullList:
		print 'Client Pulling Down:'
		print p
		ff = next((item for item in clientIndex['fileList'] if item['ID'] == p),None)
		#sendPath = stripBase(path, ff['path'])
		msg = {'username': username, 'ID': str(p)}
		#print msg
		print ff['path']
		pullFilePost(msg, ff['path'])
		
	for d in fileDeleteList:
		#print 'Deleting File:'
		#print d
		msg = {'username': username, 'ID': str(d)}
		#print msg
		fileDeletePost(msg)
	for d in dirDeleteList:
		#print 'dirDeleteList'
		#print d
		msg = {'username': username, 'ID': str(d)}
		#print msg
		dirDeletePost(msg)
	for u in updatelist:
		print 'Client sending update:'
		sendPath = stripBase(path, u['path'])
		msg = {'username': username, 'ID': str(u['ID']), 'path': sendPath, 'time': str(u['time'])} 
		print u['path']
		updatePost(msg, u['path'])
	for dc in dcreatelist:
		print 'Creating Directoy'
		sendPath = stripBase(path, dc['path'])
		msg = {'username': username, 'ID': str(dc['ID']), 'path': sendPath}
		print sendPath
		print msg
		dirCreatePost(msg)
	for fc in fcreatelist:
		print 'Creating File'
		sendPath = stripBase(path, fc['path'])
		msg = {'username': username, 'ID': str(fc['ID']), 'path': sendPath, 'time': str(fc['time'])}
		print sendPath
		fileCreatePost(msg, fc['path'])

	
def pullFilePost(msg, path):
	r = requests.post('http://localhost:8000/syncfolder/pull', files = msg)
	with open(path, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
	#fil = open (r['path'], 'w')
	#fil.write(r['data'])
	#fil.close()
	#ff = next((item for item in clientIndex['dirList'] if item['ID'] == r['ID']),None)
	#if ff is not None:
		#path = path + r['path']
		#statbuf = os.stat(path)
                #t = statbuf.st_mtime
		#ff['localTime'] = t


def fileDeletePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/fileDelete', files = msg)


def dirDeletePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/dirDelete', files = msg)


def updatePost(msg, fullPath):
	msg['file'] = open(fullPath, 'rb')
	r = requests.post('http://localhost:8000/syncfolder/update', files = msg)
	

def dirCreatePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/dirCreate', files = msg)
	

def fileCreatePost(msg, fullPath):
	msg['file'] = open(fullPath, 'rb')
	r = requests.post('http://localhost:8000/syncfolder/fileCreate', files = msg)
	

def fullSync(path, username, savePath):
	systemDir = getSystemDir(path)
	#print 'SYSTEM DIRECT ----------------------'
	#print systemDir
	clientIndex = getClientIndex(username, savePath)
	print 'CLIENT INDEX ----------------------------'
	print clientIndex
	deleteList = createDeleteList(clientIndex)

	fileDeleteList = deleteList['fileDeleteList']
	#print 'FILE DELETE -------------'
	#print fileDeleteList
	dirDeleteList = deleteList['dirDeleteList']
	lists = systemClientCompare(clientIndex, systemDir)
	#print 'FILE CREATE --------------------'
	#print lists['fcreatelist']
	serverIndex = getServerIndex(username, savePath)
	print 'SERVER INDEX -------------------------------'
	print serverIndex
	pullList = clientServerCompare(clientIndex, serverIndex, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], path, savePath, username)
	sendPosts(clientIndex, pullList, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], username, path)
	saveClientIndex(clientIndex, username, savePath)
	
def stripBase(basePath, objectPath):
	p = objectPath.split(basePath)
	#print 'STRIP PATH -------------------------------------'
	#print basePath
	#print objectPath
	#print p
	return p[1]

def purgeList(savePath, username):
	print 'Purging: ' + savePath+str(username)+'.pkl'
	file2 = open(savePath+str(username)+'.pkl', 'rb')
    	index = pickle.load(file2)
    	file2.close()
	for f in index['fileList']:
		index['fileList'].remove(f)
	for d in index['dirList']:
		index['dirList'].remove(d)
	print index
	savData = open(savePath+str(username)+'.pkl', 'rb')
    	pickle.dump(index, savData)
    	savData.close()	
		

def runLoop(path, username, savePath):
	try:
		while True:
			fullSync(path, username, savePath)
     			time.sleep(1)

	except KeyboardInterrupt:
        	print 'Stop'
		sys.exit
				
if __name__ == "__main__":
			

	#username = raw_input("Enter Username: ")
	username = 'kevin'
	#path = raw_input("Enter Watched directory: ")
	path = '/home/student/html'
	#savePath = raw_input("Enter saveData path: ")
	savePath = '/home/student/saveData2/'
	#fullSync(path, username, savePath)
	try:
		while True:
			fullSync(path, username, savePath)
     			#time.sleep(1)

	except KeyboardInterrupt:
        	print 'Turn syncronize on? [y/n] '
		time.sleep(1)

	
	#purgeList(savePath, username)
	#savePath = '/home/student/saveData2/'
	#purgeList(savePath, username)
	#savePath = '/home/student/dropserver/fileIndexes/'
	#purgeList(savePath, username)

	#p = stripBase('/home/student/watch', '/home/student/watch/fileD/file')
	#print p
	#f = getServerIndex(username)
	#print f
	#sysDir = getSystemDir(p)
	#pumpServerIndexTest(savePath, username, sysDir)
	
	#try:
	#	while True:
     	#		time.sleep(1)
	#		fullSync(p, username, savePath)
	#except KeyboardInterrupt:
        #	print 'Stop'
	#	sys.exit

#sysD = getSystemDir(p)
#pumpIndexTest('/home/student/saveData', username, sysD)
#pumpServerIndexTest('/home/student/saveData', username, sysD)
#server = getClientIndex(username+'Server', savePath)
#client = getClientIndex(username, savePath)
#delete = createDeleteList(client)
#for d in sysD['dirs']:
	#print d['path']
#for f in sysD['files']:
	#print f['path']
	#print f['modTime']
#print '------------------------'
#for d in server['dirList']:
	#print d['path']
#for f in server['fileList']:
	#print f['path']
	#print f['localTime']

#lists = systemClientCompare(client, sysD)
#print '================================='
#print 'DELETE LIST'
#print delete
#print client
#print 'DCREATE LIST'
#print lists['dcreatelist']
#print 'FCREATE LIST'
#print lists['fcreatelist']
#print 'UPDATE LIST'
#print lists['updatelist']
