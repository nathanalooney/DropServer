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
	direct = os.getcwd
	f = {'username': 'kevin', 'fileList': [], 'dirList':[]}
	idN = 1
	for d in sysD['dirs']:
		f['dirList'].append({'path': d['path'], 'ID':idN})
		idN = idN + 1
	for fil in sysD['files']:
		f['fileList'].append({'path': fil['path'], 'ID':idN, 'time': fil['modTime']})
		idN = idN + 1

	savData = open(path+str(username)+'Server'+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f


def getClientIndex(username, savePath):
	try: 
		file2 = open(savePath+str(username)+'.pkl', 'rb')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
	except IOError:
    		direct = os.getcwd
		fi = {'username':username, 'fileList': [], 'dirList': []}
    		savData = open(savePath+str(username)+'.pkl', 'wb')
    		pickle.dump(fi, savData)
    		savData.close()
		file2 = open(savePath+str(username)+'.pkl', 'rb')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex


def saveClientIndex(clientIndex, username, savePath):
	savData = open(savePath+str(username)+'.pkl', 'wb')
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
			fileDeleteList.append(f['ID'])
			clientIndex['fileList'].remove(f)
	return {'fileDeleteList': fileDeleteList, 'dirDeleteList': dirDeleteList}

def getServerIndex(username):
	msg = {'username': username}
	r = requests.post('http://localhost:8000/syncfolder/getServerIndex', files = msg)
	fil = open (savePath+str(username)+'Server'+'.pkl', 'w')
	fil.write(r['data'])
	fil.close()
	serverFile = open(savePath+str(username)+'Server'+'.pkl', 'rb')
    	serverIndex = pickle.load(file2)
    	file2.close()
	os.remove(savePath+str(username)+'Server'+'.pkl')
	return serverIndex

def systemClientCompare(clientIndex, systemDict):
	dcreatelist = []
	fcreatelist = []
	updatelist = []
	for dirs in systemDict['dirs']:
		ff = next((item for item in clientIndex['dirList'] if item['path'] == dirs['path']),None)
		if ff is None:
			print 'directory not found: ' + str(dirs['path'])
			dcreatelist.append({'path': dirs['path']})
	for fils in systemDict['files']:
		ff = next((item for item in clientIndex['fileList'] if item['path'] == fils['path']),None)
		if ff is None:
			print 'file not found: ' + str(fils['path'])
			fcreatelist.append({'path':fils['path'], 'time':fils['modTime']})
		else:
			print 'this is filefound: ' + str(ff)
			if ff['localTime'] < fils['modTime']:
				ff['localTime'] = fils['modTime']
				updatelist.append({'ID': ff['ID'], 'time': ff['localTime'], 'path': ff['path']})
	return {'dcreatelist': dcreatelist, 'fcreatelist': fcreatelist, 'updatelist': updatelist}

def clientServerCompare(clientIndex, serverIndex, deletelist, updatelist, dcreatelist, fcreatelist, path):
	largeID = 0
	clientPullList = []
	for d in serverIndex['dirList']:
		if d['ID'] > largeID:
			largeID = d['ID']
		dd = next((item for item in clientIndex['dirList'] if item['ID'] == d['ID']),None)
		if dd is None:
			if d['ID'] not in deletelist:
				#create the directory here, dont actually need to pull it
				os.mkdir(path + d['path'])
				clientIndex['dirList'].append({'path':d['path'], 'ID':d['ID']})
	for f in serverIndex['fileList']:
		if f['ID'] > largeID:
			largeID = f['ID']
		ff = next((item for item in clientIndex['fileList'] if item['ID'] == d['ID']),None)
		if ff is None:
			if f['ID'] not in deletelist:
				clientIndex['fileList'].append({'path':f['path'], 'ID':f['ID'], 'serverTime':f['time'], 'localTime':f['time']})
				clientPullList.append(f['ID'])
		else:
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
			os.rmdir(d['path'])
			clientIndex['dirList'].remove(f)
	for d in dcreatelist:
		d['ID'] = largeID + 1
		clientIndex['dirList'].append({'ID':d['ID'], 'path': d['path']})
		largeID = largeID + 1
	for f in fcreatelist:
		f['ID'] = largeID + 1
		clientIndex['fileList'].append({'ID':f['ID'], 'path': f['path'], 'localTime': f['modTime'], 'serverTime':f['modTime']})
		largeID = largeID +1

	return clientPullList


def sendPosts(clientPullList, fileDeletelist, dirDeleteList, updatelist, dcreatelist, fcreatelist, username, path):
	q = []
	for p in clientPullList:
		msg = {'username': username, 'ID': p['ID']}
		pullFilePost(msg, path)
	for d in fileDeletelist:
		msg = {'username': username, 'ID': d['ID']}
		fileDeletePost(msg)
	for d in dirDeletelist:
		msg = {'username': username, 'ID': d['ID']}
		dirDeletePost
	for u in updatelist:
		msg = {'username': username, 'ID': u['ID'], 'path': u['path'], 'time': u['time']} 
		updatePost(msg)
	for dc in dcreatelist:
		msg = {'username': username, 'ID': dc['ID'], 'path': dc['path']}
		dirCreatePost(msg)
	for fc in fcreatelist:
		msg = {'username': username, 'ID': fc['ID'], 'path': fc['path'], 'time': fc['time']}
		fileCreatePost(msg)

	
def pullFilePost(msg, path):
	r = requests.post('http://localhost:8000/syncfolder/pull', files = msg)
	fil = open (r['path'], 'w')
	fil.write(r['data'])
	fil.close()
	ff = next((item for item in clientIndex['dirList'] if item['ID'] == r['ID']),None)
	if ff is not None:
		path = path + r['path']
		statbuf = os.stat(path)
                t = statbuf.st_mtime
		ff['localTime'] = t


def fileDeletePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/fileDelete', files = msg)


def dirDeletePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/dirDelete', files = msg)


def updatPost(msg):
	msg['file'] = open(msg['path'], 'rb')
	r = requests.post('http://localhost:8000/syncfolder/update', files = msg)
	

def dirCreatePost(msg):
	r = requests.post('http://localhost:8000/syncfolder/dirCreate', files = msg)
	

def fileCreatePost(msg):
	msg['file'] = open(msg['path'], 'rb')
	r = requests.post('http://localhost:8000/syncfolder/fileCreate', files = msg)
	

def fullSync(path, username, savePath):
	systemDir = getSystemDir(path)
	clientIndex = getClientIndex(username, savePath)
	deleteList = createDeleteList(clientIndex)
	fileDeleteList = deleteList['fileDeleteList']
	dirDeleteList = deleteList['dirDeleteList']
	lists = systemClientCompare(clientIndex, systemDir)
	serverIndex = getServerIndex(username)
	pullList = clientServerCompare(clientIndex, serverIndex, fileDeletelist, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], path)
	sendPosts(pullList, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'], username, path)
	saveClientIndex(clientIndex, username, savePath)
	
			
		
				
if __name__ == "__main__":
			
	username = 'kevin'
	p = '/home/student/html'
	savePath = '/home/student/saveData'
	try:
		while True:
     			time.sleep(1)
			fullSync(p, username, savePath)
	except KeyboardInterrupt:
        	print 'Stop'
		sys.exit

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
