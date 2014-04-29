__author__ = 'Rahim'

import Tkinter
import sqlite3
import csv
import sync
import requests


class simpleapp_tk(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.winfo_parent()
        self.initialize()

    def initialize(self):
        self.minsize(300,200)
        self.maxsize(600,400)
        self.grid()
        self.title("Login")
        self.nameVariable = Tkinter.StringVar()
        self.passwordVariable = Tkinter.StringVar()
        self.nameEntry = Tkinter.Entry(self,textvariable=self.nameVariable)
        self.nameEntry.bind("<Return>", self.OnPressEnter)

        self.passwordEntry = Tkinter.Entry(self, textvariable=self.passwordVariable, show='*')
        self.passwordEntry.bind("<Return>", self.OnPressEnter)
        self.nameEntry.grid(column=0,row=1,sticky='EW')
        self.passwordEntry.grid(column=0,row=3,sticky='EW')

        button = Tkinter.Button(self,text=u"Enter !", command=self.OnButtonClick)
        button.grid(column=0,row=4)


        button2 = Tkinter.Button(self, text=u"New User ?", command=self.OnButtonClick2)
        button2.grid(column=0,row=8)

        self.labelVariable2 = Tkinter.StringVar()
        label2 = Tkinter.Label(self,textvariable=self.labelVariable2,
                              anchor="w",fg="black")
        label2.grid(column=0,row=2,columnspan=2,sticky='EW')
        self.labelVariable2.set(u"Password")

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="black")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Name")

        self.grid_columnconfigure(0,weight=1)
        self.grid_size()
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())


    def OnButtonClick(self):
	print 'Enter'
        tempName = self.nameEntry.get()
        tempPass = self.passwordEntry.get()
	files = {'username': tempName, 'password': tempPass}
        #Logic for server requests and in validation
	r = requests.post("http://localhost:8000/syncfolder/login", files=files)
	resp = r.text
	print resp
	if resp == "Success":
		self.initializeDirectoryWind()
        #if tempPass == "poofart" and tempName == "kevin":
            #self.initializeSuccess()
	elif resp =="Admin":
		self.getAllFiles()
        else:
            	self.initializeFailure()


    def dirInitButton(self, event):
        self.initializeDirectoryWind()



    def initializeDirectoryWind(self):
        u = Tkinter.Toplevel()
        u.title("Directories")
        u.minsize(300,200)
        u.maxsize(300,200)

        u.labelVar = Tkinter.StringVar()
        u.label = Tkinter.Label(u, textvariable=u.labelVar,  anchor="w",fg="black")
        u.label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.watchVar = Tkinter.StringVar()
        u.labelVar.set(u"Watch Directory")
        self.WatchEntry = Tkinter.Entry(u,textvariable=self.watchVar)
        self.WatchEntry.grid(column=0,row=2,columnspan=2,sticky='EW')




        u.label2Var = Tkinter.StringVar()
        u.label2 = Tkinter.Label(u, textvariable=u.label2Var,  anchor="w",fg="black")
        u.label2.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.saveVar = Tkinter.StringVar()
        u.label2Var.set(u"Save Directory")
        self.saveVarEntry = Tkinter.Entry(u,textvariable=self.saveVar)
        self.saveVarEntry.grid(column=0,row=6,columnspan=2,sticky='EW')



        u.button = Tkinter.Button(u,text=u"Syncronize!", command=self.initializeSuccess)
        u.button.grid(column=0,row=8)
        u.button2 = Tkinter.Button(u,text=u"Change password!", command=self.passChange)
        u.button2.grid(column=0,row=12)

    def passChange(self):
        u = Tkinter.Toplevel()
        u.title("Change Pass")
        u.minsize(300,200)
        u.maxsize(300,200)

        u.labelVar = Tkinter.StringVar()
        u.label = Tkinter.Label(u, textvariable=u.labelVar,  anchor="w",fg="black")
        u.label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.newpassVar = Tkinter.StringVar()
        u.labelVar.set(u"New Password")
        self.newpassEntry = Tkinter.Entry(u,textvariable=self.newpassVar)
        self.newpassEntry.grid(column=0,row=2,columnspan=2,sticky='EW')

        u.button2 = Tkinter.Button(u,text=u"Change password!", command=self.changePassword)
        u.button2.grid(column=0,row=5)

    def changePassword(self):
        newpass =self.newpassVar;
        files = {'password':newpass}
        r = requests.post("http://localhost:8000/syncfolder/changePassword", files=files)
        resp = r.txt
        print resp
        if resp == "Success":
            print "password changed!"
        else:
            print "password change failed!"





    def OnPressEnter(self, event):
	print 'Enter'
        tempName = self.nameEntry.get()
        tempPass = self.passwordEntry.get()
	files = {'username': tempName, 'password': tempPass}
        #Logic for server requests and in validation
	r = requests.post("http://localhost:8000/syncfolder/login", files=files)
	resp = r.text
	print resp
	if resp == "Success":
		self.initializeDirectoryWind()
        #if tempPass == "poofart" and tempName == "kevin":
            #self.initializeSuccess()
	elif resp =="Admin":
		self.getAllFiles()
        else:
            self.initializeFailure()

    def getAllFiles(self):
	r = requests.post("http://localhost:8000/syncfolder/getAll", files={})
	l = Tkinter.Toplevel()
        l.minsize(400,400)
        l.maxsize(600,800)
        l.title(u"Admin File List")

        l.labelVar2 = Tkinter.StringVar()
        l.label2 = Tkinter.Label(l, textvariable=l.labelVar2, anchor="w", fg="black")
        l.label2.grid(column=1, row=1, columnspan=1, sticky='EW')
        l.labelVar2.set(u"Files")


        l.listbox = Tkinter.Listbox(l, width=200)
        l.listbox.grid(column=0, row=0, columnspan=110, rowspan=120, sticky='EWNS')

	
	j = r.text.split('\n')
	#print j
	i =0
        for item in j:
           	#print j['path']
		l.listbox.insert(i, item)
		i = i+1
            #Add the list of Queries of file names from DB



	

    def RegEnter(self):
        print 'Register User'
	files = {'username': str(self.nameEntry.get()), 'password': str(self.passwordEntry.get())}
	r = requests.post("http://localhost:8000/syncfolder/setup", files=files)
	if r.text == "Success":
		print 'Success'
		self.initializeDirectoryWind()
	else:
		self.initializeRegFailure()


    def OnButtonClick2(self):
        self.regWindow()


    def initializeFailure(self):
        t = Tkinter.Toplevel()
        t.title("Warning")
        t.minsize(175,50)
        t.maxsize(175,50)
        t.labelVar = Tkinter.StringVar()
        t.label = Tkinter.Label(t, textvariable=t.labelVar,  anchor="w",fg="black")
        t.label.grid(column=1,row=1,columnspan=2,sticky='EW')
        t.labelVar.set(u"Invalid Username and Password")

    def initializeRegFailure(self):
        t = Tkinter.Toplevel()
        t.title("Warning")
        t.minsize(175,50)
        t.maxsize(175,50)
        t.labelVar = Tkinter.StringVar()
        t.label = Tkinter.Label(t, textvariable=t.labelVar,  anchor="w",fg="black")
        t.label.grid(column=1,row=1,columnspan=2,sticky='EW')
        t.labelVar.set(u"Failure: Username Exists")



    def initializeSuccess(self):
	print self.nameEntry.get()
	print self.saveVarEntry.get()
        sync.fullSync(self.WatchEntry.get(), self.nameEntry.get(), self.saveVarEntry.get())
        l = Tkinter.Toplevel()
        l.minsize(400,400)
        l.maxsize(600,600)
        l.title(u"FallCube -- Home")
        l.labelVar = Tkinter.StringVar()
        l.label = Tkinter.Label(l, textvariable=l.labelVar, anchor="w", fg="black")
        l.label.grid(column=0, row=0, columnspan=1, sticky='EW')
        l.labelVar.set(u"Welcome " + self.nameEntry.get() + u"!")

        l.labelVar2 = Tkinter.StringVar()
        l.label2 = Tkinter.Label(l, textvariable=l.labelVar2, anchor="w", fg="black")
        l.label2.grid(column=1, row=1, columnspan=1, sticky='EW')
        l.labelVar2.set(u"Files")

        l.labelVar3 = Tkinter.StringVar()
        l.label3 = Tkinter.Label(l, textvariable=l.labelVar3, anchor="w", fg="black")
        l.label3.grid(column=2, row=1, columnspan=1, sticky='EW')
        l.labelVar3.set(u"Directories")

        l.listbox = Tkinter.Listbox(l)
        l.listbox.grid(column=0, row=2, columnspan=10, rowspan=6, sticky='EW')
	
        k = ["look", "I am ", "adding to", "the listbox"]
	j = sync.getClientIndex(self.nameEntry.get(), self.saveVarEntry.get())
	print j
	i =0
        for item in j['fileList']:
           	#print j['path']
		l.listbox.insert(i, item['path'])
		i = i+1
            #Add the list of Queries of file names from DB

        l.listbox2 = Tkinter.Listbox(l)
        l.listbox2.grid(column=11, row=2, columnspan=20, rowspan=10, sticky='EW')

        l.button = Tkinter.Button(l, text=u"Syncronize", command=self.syncronize)
        l.button.grid(column=0,row=12)
	i =0
        for item in j['dirList']:
           	#print j['path']
		l.listbox2.insert(i, item['path'])
		i = i+1

    def syncronize(self):
        #Dont quite know the path names but this will do for now
      #  sync.fullSync(self.watchDir, self.nameEntry.get(), self.saveDir)
        #add logic for syncronizing and updating
        sync.runLoop(self.WatchEntry.get(), self.nameEntry.get(), self.saveVarEntry.get())


    def regWindow(self):
        o = Tkinter.Toplevel()
        o.minsize(300,200)
        o.maxsize(600,400)
        o.title("Registration")
        self.nameVariable = Tkinter.StringVar()
        self.passwordVariable = Tkinter.StringVar()
        o.passwordConfirm = Tkinter.StringVar()
        o.watchDirectory = Tkinter.StringVar()
        o.saveDir = Tkinter.StringVar()

        self.nameEntry = Tkinter.Entry(o, textvariable=self.nameVariable)
        self.nameEntry.bind("<Return>",self.RegEnter)
        self.passwordEntry = Tkinter.Entry(o, textvariable=self.passwordVariable, show='*')
        self.passwordEntry.bind("<Return>",self.RegEnter)
        o.confirmpasswordEntry = Tkinter.Entry(o, textvariable=o.passwordConfirm, show='*')
        o.confirmpasswordEntry.bind("<Return>",self.RegEnter)
        self.nameEntry.grid(column=0,row=1,sticky='EW')
        self.passwordEntry.grid(column=0,row=3,sticky='EW')
        o.confirmpasswordEntry.grid(column=0,row=5,sticky='EW')


        o.labelVariable2 = Tkinter.StringVar()
        label2 = Tkinter.Label(o,textvariable=o.labelVariable2,
                              anchor="w",fg="black")
        label2.grid(column=0,row=2,columnspan=2,sticky='EW')
        o.labelVariable2.set(u"Password")

        o.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(o,textvariable=o.labelVariable,
                              anchor="w",fg="black")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        o.labelVariable.set(u"Name")

        o.labelVariable3 = Tkinter.StringVar()
        label3 = Tkinter.Label(o,textvariable=o.labelVariable3,
                              anchor="w",fg="black")
        label3.grid(column=0,row=4,columnspan=2,sticky='EW')
        o.labelVariable3.set(u"Confirm Password")

        o.button = Tkinter.Button(o,text=u"Enter !", command=self.OnButtonClickReg)
        o.button.grid(column=0,row=10)



    def OnButtonClickReg(self):
	print 'Register User'
	files = {'username': str(self.nameEntry.get()), 'password': str(self.passwordEntry.get())}
	r = requests.post("http://localhost:8000/syncfolder/setup", files=files)
	if r.text == "Success":
		print 'Success'
		self.initializeDirectoryWind()
	else:
		self.initializeRegFailure()
	
        #print"Im chillin big brother Im chillin"
        #Enter logic for checking to see if in DB and also add to db;
        #also validate password logic and



if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.mainloop()


