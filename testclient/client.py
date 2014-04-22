__author__ = 'Boyang'
import urllib2
import requests
import json
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
#from syncfolder.models import Users
import os
import fileObj
class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        statbuf = os.stat(event.src_path)
        t = statbuf.st_mtime
        f = fileObj.fileObj(event.src_path,t,3)
        jstring = json.dumps(f.toDict())
        files = {'type': 'created', 'fileObj': jstring, 'data': open(event.src_path, 'rb')}
        #dict = json.loads(jstr)
        #newfil = fileObj.fileObj(files['path'],files['time'],files['id'])
        r = requests.post('http://localhost:8000/syncfolder/send', files = files)
        print "Sent successfully!"


    def on_modified(self, event):
        print("Event type: " + event.event_type + "\n Is it a directory?:" + str(event.is_directory) + "\n Path of file changed: " + str(event.src_path))
        files = {'file': open(event.src_path, 'rb')}
        r = requests.post('http://localhost:8000/syncfolder/send', files = files)
        print "Sent successfully!"



    def on_deleted(self,event):
        print("Event type: " + event.event_type + "\n Is it a directory?:" + str(event.is_directory) + "\n Path of file changed: " + str(event.src_path))
        print("\n Delete not yet implemented.")




if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'dropbox.settings'
    #x = Users(username = "boyang", email = "bh3ay@virginia.edu", password = "password", rootdirectory = "C:\Users\Boyang\Desktop\3240_testfolder")
    #x.save()
    #user = sys.argv[2]
    #password = sys.argv[3]
    #tempdict=Users.objects.filter(username = user, password = password).values()
    #if tempdict.len() != 0:
    #    print "successful login"
    #else:
    #    print "failed login"
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    files = {'file': open('testfile.txt', 'rb')}
    r = requests.post('http://localhost:8000/syncfolder/send', files = files)
    print "Successful send!"




    
