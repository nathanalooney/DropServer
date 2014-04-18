__author__ = 'Kevin'

import fileObj
class FileIndex:

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

