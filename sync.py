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
import sys
import requests


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
	return {'dirs': direct, 'files': fil}

def pumpIndexTest(path, username, sysDir):
	direct = os.getcwd
	f = {'username': 'kevin', 'fileList': [], 'dirList':[]}
	idN = 1
	for d in sysDir['dirs']:
		f['dirList'].append({'path': d['path'], 'ID':idN})
		idN = idN + 1
	for fil in sysDir['files']:
		f['fileList'].append({'path': fil['path'], 'ID':idN, 'localTime': fil['modTime'], 'serverTime': fil['modTime']})
		idN = idN + 1

	savData = open(path+str(username)+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f

def pumpServerIndexTest(path, username, sysDir):
	f = {'username': 'kevin', 'fileList': [], 'dirList':[]}
	idN = 1
	savData = open(path+str(username)+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f


def getClientIndex(username, savePath):
	if os.path.exists(str(savePath).rstrip('/') + '/'+str(username)+'.pkl'):
		file2 = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
	else:

		fi = {'username':username, 'fileList': [], 'dirList': []}
    		savData = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'wb')
    		pickle.dump(fi, savData)
    		savData.close()
		time.sleep(1)
		file2 = open(str(savePath).rstrip('/') + '/'+str(username)+'.pkl', 'r+b')
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
			dirDeleteList.append(d['ID'])
			clientIndex['dirList'].remove(d)
	for f in clientIndex['fileList']:
		if not os.path.exists(str(f['path'])):
			fileDeleteList.append(f['ID'])
			clientIndex['fileList'].remove(f)
	return {'fileDeleteList': fileDeleteList, 'dirDeleteList': dirDeleteList}

def getServerIndex(username, savePath, ip):
	msg = {'username': username}
	r = requests.post(str(ip)+'/syncfolder/getServerIndex', files = msg)
	with open(savePath+str(username)+'Server'+'.pkl', 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()
	serverFile = open(savePath+str(username)+'Server'+'.pkl', 'rb')
    	index = pickle.load(serverFile)
    	serverFile.close()
	os.remove(savePath+str(username)+'Server'+'.pkl')
	for d in index['dirList']:
		temp = d['ID']
		d['ID'] = str(temp)
	return index

def systemClientCompare(clientIndex, systemDict):
	dcreatelist = []
	fcreatelist = []
	updatelist = []
	for dirs in systemDict['dirs']:
		ff = next((item for item in clientIndex['dirList'] if item['path'] == dirs['path']),None)
		if ff is None:
			dcreatelist.append({'path': dirs['path']})
	for fils in systemDict['files']:
		ff = next((item for item in clientIndex['fileList'] if item['path'] == fils['path']),None)

		if ff is None:
			fcreatelist.append({'path':fils['path'], 'time':fils['modTime']})
		else:
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
				if not os.path.exists(str(path) + '/' + str(d['path']).lstrip('/')):
					os.mkdir(str(path) + '/' + str(d['path']).lstrip('/'))
					clientIndex['dirList'].append({'path':d['path'], 'ID':d['ID']})
	for f in serverIndex['fileList']:
		if f['ID'] > largeID:
			largeID = f['ID']
		ff = next((item for item in clientIndex['fileList'] if int(item['ID']) == int(f['ID'])),None)
		if ff is None:
			if f['ID'] not in fileDeleteList:
				clientIndex['fileList'].append({'path':str(path)+'/'+str(f['path']).lstrip('/'), 'ID':f['ID'], 'serverTime':f['time'], 'localTime':f['time']})
				clientPullList.append(f['ID'])
		else:
			if f['time'] > ff['serverTime']:
				clientPullList.append(f['ID'])
				ff['serverTime'] = f['time'] 
				if f['ID'] in updatelist:
					updatelist.remove(f['ID'])
	for f in clientIndex['fileList']:	
		ff = next((item for item in serverIndex['fileList'] if item['ID'] == f['ID']),None)
		if ff is None:
			if os.path.exists(f['path']):
				os.remove(f['path'])
			clientIndex['fileList'].remove(f)
	for d in clientIndex['dirList']:	
		dd = next((item for item in serverIndex['dirList'] if item['ID'] == d['ID']),None)
		if dd is None:
			try:
				os.rmdir(d['path'])
				clientIndex['dirList'].remove(d)
			except OSError:
				i = 0
	for d in dcreatelist:
		d['ID'] = str(int(largeID) + 1)
		clientIndex['dirList'].append({'ID':d['ID'], 'path': d['path']})
		largeID = int(largeID) + 1
	for f in fcreatelist:
		f['ID'] = str(int(largeID) + 1)
		clientIndex['fileList'].append({'ID':f['ID'], 'path': f['path'], 'localTime': f['time'], 'serverTime':f['time']})
		largeID = int(largeID) +1
	
	saveClientIndex(clientIndex, username, savePath)

	return clientPullList


def sendPosts(clientIndex, clientPullList, fileDeleteList, dirDeleteList, updatelist, dcreatelist, fcreatelist, username, path, ip):
	q = []
	for p in clientPullList:
		ff = next((item for item in clientIndex['fileList'] if item['ID'] == p),None)
		msg = {'username': username, 'ID': str(p)}
		pullFilePost(msg, ff['path'], ip)
		
	for d in fileDeleteList:
		msg = {'username': username, 'ID': str(d)}
		fileDeletePost(msg, ip)
	for d in dirDeleteList:
		msg = {'username': username, 'ID': str(d)}
		dirDeletePost(msg, ip)
	for u in updatelist:
		sendPath = stripBase(path, u['path'])
		msg = {'username': username, 'ID': str(u['ID']), 'path': sendPath, 'time': str(u['time'])} 
		updatePost(msg, u['path'], ip)
	for dc in dcreatelist:
		sendPath = stripBase(path, dc['path'])
		msg = {'username': username, 'ID': str(dc['ID']), 'path': sendPath}
		dirCreatePost(msg, ip)
	for fc in fcreatelist:
		sendPath = stripBase(path, fc['path'])
		msg = {'username': username, 'ID': str(fc['ID']), 'path': sendPath, 'time': str(fc['time'])}
		fileCreatePost(msg, fc['path'], ip)

	
def pullFilePost(msg, path, ip):
	r = requests.post(str(ip)+'/syncfolder/pull', files = msg)
	with open(path, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				f.flush()


def fileDeletePost(msg, ip):
	r = requests.post(str(ip)+'/syncfolder/fileDelete', files = msg)


def dirDeletePost(msg, ip):
	r = requests.post(str(ip)+'/syncfolder/dirDelete', files = msg)


def updatePost(msg, fullPath, ip):
	if os.path.exists(str(fullPath)):
		msg['file'] = open(fullPath, 'rb')
		r = requests.post(str(ip)+'/syncfolder/update', files = msg)
	

def dirCreatePost(msg, ip):
	r = requests.post(str(ip)+'/syncfolder/dirCreate', files = msg)
	

def fileCreatePost(msg, fullPath, ip):
	if os.path.exists(str(fullPath)):
		msg['file'] = open(fullPath, 'rb')
		r = requests.post(str(ip)+'/syncfolder/fileCreate', files = msg)
	

def fullSync(path, username, savePath, ip):
	systemDir = getSystemDir(path)
	clientIndex = getClientIndex(username, savePath)
	deleteList = createDeleteList(clientIndex)

	fileDeleteList = deleteList['fileDeleteList']
	dirDeleteList = deleteList['dirDeleteList']
	lists = systemClientCompare(clientIndex, systemDir)
	serverIndex = getServerIndex(username, savePath, ip)
	pullList = clientServerCompare(clientIndex, serverIndex, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], path, savePath, username)
	sendPosts(clientIndex, pullList, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], username, path, ip)
	saveClientIndex(clientIndex, username, savePath)
	
def stripBase(basePath, objectPath):
	p = objectPath.split(basePath)
	return p[1]

def purgeList(savePath, username):
	print 'Purging: ' + savePath+str(username)+'.pkl'
	file2 = open(savePath+str(username)+'.pkl', 'r+b')
    	index = pickle.load(file2)
    	file2.close()
	for f in index['fileList']:
		index['fileList'].remove(f)
	for d in index['dirList']:
		index['dirList'].remove(d)
	print index
	savData = open(savePath+str(username)+'.pkl', 'r+b')
    	pickle.dump(index, savData)
    	savData.close()	
		

def runLoop(path, username, savePath, ip):
	try:
		while True:
			fullSync(path, username, savePath, ip)
     			time.sleep(1)

	except KeyboardInterrupt:
        	print 'Stop'
		sys.exit
				
if __name__ == "__main__":
			
	
	#username = raw_input("Enter Username: ")
	username = 'kb'
	#path = raw_input("Enter Watched directory: ")
	path = '/home/student/html'
	#savePath = raw_input("Enter saveData path: ")
	savePath = '/home/student/save/'

	purgeList(savePath, username)
	savePath = '/home/student/save2/'
	purgeList(savePath, username)
	#savePath = '/home/student/dropserver/fileIndexes/'
	#purgeList(savePath, username)
	
