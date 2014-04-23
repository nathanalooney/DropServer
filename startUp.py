__author__ = 'Kevin'
import pickle
import fileIndex
import fileObj
import dirObj
import os
import json



def loadIndex():
    direct = os.getcwd
    #base = os.path.abspath(direct)
    fi = fileIndex.File_Index('kevin', direct)

    savData = open(r'D:\OneDir\data.pkl', 'wb')
    pickle.dump(fi, savData)
    savData.close()

    file2 = open(r'D:\OneDir\data.pkl', 'rb')
    newIndex = pickle.load(file2)
    file2.close()
    return newIndex

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
    	

def getServerIndex():
	print 'grab the index from server'

def createClientDeleteList(clientIndex):
	retList = []
	for dirs in clientIndex['fileList']:
		path = dirs['path']
		if not os.path.exists(path):
			retList.append(dirs)
			clientIndex['fileList'].remove(dirs)
	return retList

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




		#(item for item in clientIndex['dirList'] if item['path'] == dirs['path']
		#if dirs['path'] not in clientIndex['dirList']
			#clientIndex['dirlist'].append({'path'
	#print 'do it'

def find_files(path):
    result = []
    direct = []
    fil = []
    for root, dirs, files in os.walk(path):
        if dirs not in direct:
            for d in dirs:
                dir1 = root + "/" + d
                direct.append(dir1)
        if files not in fil:
            for f in files:
                pth = root+ "/" + f
                statbuf = os.stat(pth)
                #print os.path.exists(pth)
                t = statbuf.st_mtime
                f1 = fileObj.fileObj(f,pth,t, -1)
                #print f1
                fil.append(f1)
            #print '-----'
            #print root
            #print dirs
            #print files
            #fil.append(files)

    #print direct
    #print fil

    return {'d':direct, 'f':fil}

def indexToJson(fi):
    jstring = json.dumps(fi.toDict())
    return jstring

def jsonToIndex(jstr):
    dict = json.loads(jstr)
    un = dict['username']
    bp = dict['basepath']
    f = fileIndex.File_Index('kevin' ,bp)
    for files in dict['files']:
        newfil = fileObj.fileObj(files['name'],files['path'],files['time'],files['id'])
        f.addFile(newfil)
    return f


username = 'kevin'
p = '/home/student/html'
sysD = getSystemDir(p)
#pumpIndexTest('/home/student/saveData', username, sysD)
pumpServerIndexTest('/home/student/saveData', username, sysD)
server = getClientIndex(username+'Server')
client = getClientIndex(username)
for d in sysD['dirs']:
	print d['path']
for f in sysD['files']:
	print f['path']
	print f['modTime']
print '------------------------'
for d in server['dirList']:
	print d['path']
for f in server['fileList']:
	print f['path']
	print f['localTime']

lists = systemClientCompare(client, sysD)
print '================================='
print lists['dcreatelist']
print lists['fcreatelist']
print lists['updatelist']


#direct = os.getcwd
#print direct
    #base = os.path.abspath(direct)
#fi = {'username':username, 'fileList': [], 'dirlist': []}
#print str(direct)+str(username)+'.pkl'
#savData = open(str(direct)+str(username)+'.pkl', 'wb')
#pickle.dump(fi, savData)
#savData.close()
#file2 = open(r'D:\OneDir\data.pkl', 'rb')
#newIndex = pickle.load(file2)
#print newIndex
#file2.close()
#if __name__ == "__main__":
	#path = sys.argv[1] if len(sys.argv) > 1 else '.'
#fileIndex = loadIndex()
#tup = find_files('D:\WatchedDir')
#for fil in tup['f']:
#    fileIndex.addFile(fil)

#print fileIndex
#s1 = indexToJson(fileIndex)
#print s1
#filIn = jsonToIndex(s1)
#print filIn
#for f in filIn.listFiles:
    #print f.path
#print tup[1]


