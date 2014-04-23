__author__ = 'Kevin'
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
		f['fileList'].append({'path': fil['path'], 'ID':idN, 'localTime': fil['modTime'], 'serverTime': fil['modTime']})
		idN = idN + 1

	savData = open(path+str(username)+'Server'+'.pkl', 'wb')
    	pickle.dump(f, savData)
    	savData.close()
	return f


def getClientIndex(username):
	try: 
		direct = '/home/student/saveData'
		file2 = open(str(direct)+str(username)+'.pkl', 'rb')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
	except IOError:
    		direct = os.getcwd
		fi = {'username':username, 'fileList': [], 'dirList': []}
    		savData = open(str(direct)+str(username)+'.pkl', 'wb')
    		pickle.dump(fi, savData)
    		savData.close()
		file2 = open(r'D:\OneDir\data.pkl', 'rb')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
		print 'nothing here'
    	
def createDeleteList(clientIndex):
	deletelist = []
	for d in clientIndex['dirList']:
		if not os.path.exists(d['path']):
			deletelist.append(d['ID'])
			clientIndex['dirList'].remove(d)
	for f in clientIndex['fileList']:
			deletelist.append(f['ID'])
			print f['ID']
			clientIndex['fileList'].remove(f)
	return deletelist

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
			dcreatelist.append(dirs)
	for fils in systemDict['files']:
		ff = next((item for item in clientIndex['fileList'] if item['path'] == fils['path']),None)
		if ff is None:
			print 'directory not found: ' + str(fils['path'])
			fcreatelist.append(fils)
		else:
			print 'this is filefound: ' + str(ff)
			if ff['localTime'] < fils['modTime']:
				ff['localTime'] = fils['modTime']
				updatelist.append(ff)
	return {'dcreatelist': dcreatelist, 'fcreatelist': fcreatelist, 'updatelist': updatelist}

def clientServerCompare(clientIndex, serverIndex, deletelist):
	largeID = 0
	for d in serverIndex['dirList']:
		if d['ID'] > largeID:
			largeID = d['ID']
		dd = next((item for item in clientIndex['dirList'] if item['ID'] == d['ID']),None)
		#if dd is None:
			


username = 'kevin'
p = '/home/student/html'
sysD = getSystemDir(p)
#pumpIndexTest('/home/student/saveData', username, sysD)
pumpServerIndexTest('/home/student/saveData', username, sysD)
server = getClientIndex(username+'Server')
client = getClientIndex(username)
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



