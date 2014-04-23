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

fileIndex = loadIndex()
tup = find_files('D:\WatchedDir')
for fil in tup['f']:
    fileIndex.addFile(fil)

print fileIndex
s1 = indexToJson(fileIndex)
print s1
filIn = jsonToIndex(s1)
print filIn
for f in filIn.listFiles:
    print f.path
#print tup[1]


