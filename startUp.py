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

def getSystemDir
	direct = []
    	fil = []
    	for root, dirs, files in os.walk(path):
        	if dirs not in direct:
            		for d in dirs:
                		dir1 = root + "\\" + d
				d = {'path': dir1}
                		direct.append(d)
        	if files not in fil:
            		for f in files:
                		pth = root+ "\\" + f
                		statbuf = os.stat(pth)
                		t = statbuf.st_mtime
                		f1 = {'path':pth, 'modTime':t)
                		fil.append(f1)
	return {'dirs': direct, 'files': fil}
   

def getClientIndex(username):
    	direct = os.getcwd
    #base = os.path.abspath(direct)
    	fi = {'username':username, 'fileList': [], 'dirlist': []}

    	savData = open(str(direct)+str(username)+'.pkl', 'wb')
    	pickle.dump(fi, savData)
    	savData.close()
	try: 
		file2 = open(str(direct)+str(username)+'.pkl', 'rb')
    		newIndex = pickle.load(file2)
    		file2.close()
		return newIndex
	except IOError:
		fi = {'username':username, 'fileList': [], 'dirlist': []}
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
	for all dirs in clientIndex['fileList']:
		path = dirs['path']
		if not os.path.exists(path):
			retList.append(dirs)
			clientIndex['fileList'].remove(dirs)
	return retList

def systemClientCompare(clientIndex, systemDict):
	for all dirs in systemDict['dirs'

def find_files(path):
    result = []
    direct = []
    fil = []
    for root, dirs, files in os.walk(path):
        if dirs not in direct:
            for d in dirs:
                dir1 = root + "\\" + d
                direct.append(dir1)
        if files not in fil:
            for f in files:
                pth = root+ "\\" + f
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
direct = os.getcwd
print direct
    #base = os.path.abspath(direct)
fi = {'username':username, 'fileList': [], 'dirlist': []}
print str(direct)+str(username)+'.pkl'
savData = open(str(direct)+str(username)+'.pkl', 'wb')
pickle.dump(fi, savData)
savData.close()
file2 = open(r'D:\OneDir\data.pkl', 'rb')
newIndex = pickle.load(file2)
print newIndex
file2.close()
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


