__author__ = 'Kevin'
class dirObj:

    def __init__(self, name, path, time):
        self.name = name
        self.path = path
        self.ID = -1

    def setID(self, ID):
        self.ID = ID

    def setTempID(self, tempID):
        self.tempID = tempID

    def toDict(self):
        d = {'name': self.name, 'path': self.path, 'id': self.ID}
        return d
