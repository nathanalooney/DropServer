__author__ = 'Kevin'
class fileObj:

    def __init__(self, name, path, time, id):
        self.name = name
        self.path = path
        self.time = time
        self.temp_time = 0
        self.ID = id

    def setID(self, ID):
        self.ID = ID

    def setTempID(self, tempID):
        self.tempID = tempID
    def __str__(self):
        return str(self.toDict())

    def toDict(self):
        d = {'name': self.name, 'path': self.path, 'time': self.time, 'temp_time': self.temp_time, 'id': self.ID}
        return d
