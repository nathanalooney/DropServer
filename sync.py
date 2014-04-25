__author__ = 'Kevin'

#TODO fix file paths - all in client absolute right now
# figure out exactly how to do the savepath
# connection to sever/get serverIndex
# 	get real server running on other IP
# send all posts to server from queue
#	with this make sure on pulls to change local time on client index and resave
# make sure lists are being passed by reference and keeping value


import pickle
import os
import json

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
		direct = '/home/student/saveData'
		#file2 = open(str(direct)+str(username)+'.pkl', 'rb')
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
			dirDeletelist.append(d['ID'])
			clientIndex['dirList'].remove(d)
	for f in clientIndex['fileList']:
			fileDeletelist.append(f['ID'])
			#print f['ID']
			clientIndex['fileList'].remove(f)
	return {'fileDeleteList': fileDeletelist, 'dirDeleteList': dirDeleteList}

def getServerIndex():
	print 'grab the index from server'


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
			print 'directory not found: ' + str(fils['path'])
			fcreatelist.append({'path':fils['path'], 'time':fils['modTime']})
		else:
			print 'this is filefound: ' + str(ff)
			if ff['localTime'] < fils['modTime']:
				ff['localTime'] = fils['modTime']
				updatelist.append({'ID': ff['ID'], 'time': ff['localTime'], 'path': ff['path']})
	return {'dcreatelist': dcreatelist, 'fcreatelist': fcreatelist, 'updatelist': updatelist}

def clientServerCompare(clientIndex, serverIndex, deletelist, updatelist, dcreatelist, fcreatelist):
	largeID = 0
	clientPullList = []
	for d in serverIndex['dirList']:
		if d['ID'] > largeID:
			largeID = d['ID']
		dd = next((item for item in clientIndex['dirList'] if item['ID'] == d['ID']),None)
		if dd is None:
			if d['ID'] not in deletelist:
				#create the directory here, dont actually need to pull it
				os.mkdir(d['path'])
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
		
	#create all client entries for new files and directories with large ID

def fillQueue(clientPullList, fileDeletelist, dirDeleteList, updatelist, dcreatelist, fcreatelist, username):
	q = []
	for p in clientPullList:
		q.append({'type': 'pull', 'username': username, 'ID': p['ID']})
	for d in fileDeletelist:
		q.append({'type': 'fileDelete', 'username': username, 'ID': d['ID']})
	for d in dirDeletelist:
		q.append({'type': 'fileDelete', 'username': username, 'ID': d['ID']})
	for u in updatelist:
		q.append({'type': 'update', 'username': username, 'ID': u['ID'], 'path': u['path'], 'time': u['time']}) #decide where to actually grab the data
	for dc in dcreatelist:
		q.append({'type': 'dirCreate', 'username': username, 'ID': dc['ID'], 'path': dc['path']})
	for fc in fcreatelist:
		q.append({'type': 'fileCreate', 'username': username, 'ID': fc['ID'], 'path': fc['path'], 'time': fc['time']})

	
	#getServerIndex
        #r = requests.post('http://localhost:8000/syncfolder/send', files = files)
	#files = {'type': 'created', 'file': open(event.src_path, 'rb')}

def fullSync(path, username, savePath):
	systemDir = getSystemDir(path)
	clientIndex = getClientIndex(username, savePath)
	deleteList = createDeleteList(clientIndex)
	fileDeleteList = deleteList['fileDeleteList']
	dirDeleteList = deleteList['dirDeleteList']
	lists = systemClientCompare(client, systemDir)
	serverIndex = getServerIndex()
	pullList = clientServerCompare(clientIndex, serverIndex, fileDeletelist, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'])
	q = fillQueue(pullList, fileDeleteList, dirDeleteList, lists['updatelist'], lists['dcreatelist'], lists['fcreatelist'])
	saveClientIndex(clientIndex, username, savePath)
	
			
		
				
			
username = 'kevin'
p = '/home/student/html'
savePath = '/home/student/saveData'
sysD = getSystemDir(p)
#pumpIndexTest('/home/student/saveData', username, sysD)
pumpServerIndexTest('/home/student/saveData', username, sysD)
server = getClientIndex(username+'Server', savePath)
client = getClientIndex(username, savePath)
delete = createDeleteList(client)
#for d in sysD['dirs']:
	#print d['path']
#for f in sysD['files']:
	#print f['path']
	#print f['modTime']
print '------------------------'
#for d in server['dirList']:
	#print d['path']
#for f in server['fileList']:
	#print f['path']
	#print f['localTime']

lists = systemClientCompare(client, sysD)
print '================================='
print 'DELETE LIST'
print delete
print client
print 'DCREATE LIST'
print lists['dcreatelist']
print 'FCREATE LIST'
print lists['fcreatelist']
print 'UPDATE LIST'
print lists['updatelist']



