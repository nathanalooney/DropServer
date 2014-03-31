from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from pathlib import Path
import requests


# Create your views here.
def index(request):
	return HttpResponse("<h1> Index </h1>")

def send(request):
	print("Request received!")
	if request.method=='POST':
		print("POST success!")
		if 'file' in request.FILES:
			fd = request.FILES['file']
			filename = fd.name
			print filename
			fl = open(filename, 'wb')
			print("File opened!")
			data = fd.read()
			fl.write(data)
			print("File read!")
			fl.close
	return HttpResponse("<h1> Send </h1>")

def remove(request):
	return HttpResponse("<h1> Remove </h1>")

def update(request):
	return HttpResponse("<h1> Update </h1>")