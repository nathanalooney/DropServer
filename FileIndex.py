__author__ = 'Kevin'

import fileObj
import dirObj
class File_Index:

    tempIdBase = 0
    def __init__(self, username, basePath):
        self.username = username
        self.basePath = basePath
        self.listFiles = []
        self.listDirs = []

    def addFile(self, fileObj):
        self.listFiles.append(fileObj)

    def addDir(self, dirObj):
        self.listDirs.append(dirObj)
    def getUsername(self):
        return self.username

    def toDict(self):
        fil = []
        for f in self.listFiles:
            fil.append(f.toDict())
        dir = []
        for di in self.listDirs:
            dir.append(di.toDict())
        d = {'username': self.username, 'basepath': str(self.basePath), 'files': fil, 'dirs': dir}
        return d

