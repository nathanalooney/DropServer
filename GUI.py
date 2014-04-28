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
        self.nameEntry.bind("<Return>", self.dirInitButton)

        self.passwordEntry = Tkinter.Entry(self, textvariable=self.passwordVariable, show='*')
        self.passwordEntry.bind("<Return>", self.dirInitButton)
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
        tempName = self.nameEntry.get()
        tempPass = self.passwordEntry.get()

        #logic for validation and server requests
        if tempPass == "poofart" and tempName == "lala":
            self.initializeDirectoryWind()

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






    def OnPressEnter(self, event):
        tempName = self.nameEntry.get()
        tempPass = self.passwordEntry.get()

        #Logic for server requests and in validation

        if tempPass == "poofart" and tempName == "kevin":
            self.initializeSuccess()


        else:
            self.initializeFailure()

    def RegEnter(self):
        print "hi"


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


    def initializeSuccess(self):
	print self.nameEntry.get()
	print self.saveVarEntry
        sync.runLoop(self.WatchEntry.get(), self.nameEntry.get(), self.saveVarEntry.get())
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
        l.label2.grid(column=1, row=0, columnspan=1, sticky='EW')
        l.labelVar.set(u"Files")

        l.listbox = Tkinter.Listbox(l)
        l.listbox.grid(column=0, row=1, columnspan=10, rowspan=6, sticky='EW')
	
        k = ["look", "I am ", "adding to", "the listbox"]
	j = sync.getClientIndex(nameEntry.get(), '/home/student/save2'
        for item in range(0,len(j)):
            l.listbox.insert(item,j[item])
            #Add the list of Queries of file names from DB

        l.listbox2 = Tkinter.Listbox(l)
        l.listbox2.grid(column=11, row=1, columnspan=20, rowspan=10, sticky='EW')

        l.button = Tkinter.Button(l, text=u"Syncronize", command=self.syncronize)
        l.button.grid(column=0,row=12)


    def syncronize(self):
        #Dont quite know the path names but this will do for now
      #  sync.fullSync(self.watchDir, self.nameEntry.get(), self.saveDir)
        #add logic for syncronizing and updating
        print ""


    def regWindow(self):
        o = Tkinter.Toplevel()
        o.minsize(300,200)
        o.maxsize(600,400)
        o.title("Registration")
        o.nameVariable = Tkinter.StringVar()
        o.passwordVariable = Tkinter.StringVar()
        o.passwordConfirm = Tkinter.StringVar()
        o.watchDirectory = Tkinter.StringVar()
        o.saveDir = Tkinter.StringVar()

        o.nameEntry = Tkinter.Entry(o, textvariable=o.nameVariable)
        o.nameEntry.bind("<Return>",self.RegEnter)
        o.passwordEntry = Tkinter.Entry(o, textvariable=o.passwordVariable, show='*')
        o.passwordEntry.bind("<Return>",self.RegEnter)
        o.confirmpasswordEntry = Tkinter.Entry(o, textvariable=o.passwordConfirm, show='*')
        o.confirmpasswordEntry.bind("<Return>",self.RegEnter)
        o.nameEntry.grid(column=0,row=1,sticky='EW')
        o.passwordEntry.grid(column=0,row=3,sticky='EW')
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
        print"Im chillin big brother Im chillin"
        #Enter logic for checking to see if in DB and also add to db;
        #also validate password logic and



if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.mainloop()


