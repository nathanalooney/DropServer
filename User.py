
__author__ = 'Rahim'
import sqlite3
import csv

class User:

    def __init__(self, names, userIDs, passwords):
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        self.name = names
        self.userID = userIDs
        self.password = passwords
        info = (names, userIDs, passwords)
        cur.execute("INSERT INTO users VALUES(?, ?, ?);", info)
        con.commit()


    def _name(self):
        return self.name



    def _name(self, names):
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        cmd = "UPDATE users SET name = " +'"' + names +'"' +" WHERE name = " + '"' +self.name +'"' + "  AND id = " +'"' + self.userID +'"' + "AND password = " + '"' + self.password + '"' + " ;"
        cur.execute(cmd)
        con.commit()
        self.name = names



    def _password(self):
        return self.password


    def _password(self, passwords):
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        cmd = "UPDATE users SET password = " +'"' + passwords +'"' +" WHERE name = " +'"' +self.name +'"' + "  AND id = " +'"' + self.userID +'"' + "AND password = " + '"' + self.password + '"' + " ;"
        cur.execute(cmd)
        con.commit()
        self.password = passwords


    def _userID(self):
        return self.userID


    def _userID(self, userIDs):
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        cmd = "UPDATE users SET id = " +'"' + userIDs +'"' +" WHERE name = " +'"' +self.name +'"' + "  AND id = " +'"' + self.userID +'"' + "AND password = " + '"' + self.password + '"' + " ;"
        cur.execute(cmd)
        con.commit()
        self.userID = userIDs

    def __str__(self):
        return '['+ self.name + ',' + self.userID + ',' + self.password + ']'



if __name__ == "__main__":
    p = User("Rahim Islam", "rji2hv", "dnakjf")
    print p.name
    p._name("kooool")
    print p.name
    print p.password
    p._password("blloowwnn")
    print p.password
    print p.userID
    p._userID("-_-")
    print p.userID