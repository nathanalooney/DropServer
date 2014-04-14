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

		if 'file' in request.FILES:
			fd = request.FILES['file']
			filename = fd.name
			path = Path(request.FILES['path'].read())
			user = request.FILES['user'].read()+'/'

			fl = open('folders/' + user + filename, 'wb')
			data = fd.read()
			fl.write(data)
			fl.close

	return HttpResponse("<h1> Send </h1>")


def remove(request):
	return HttpResponse("")


def update(request):
	return HttpResponse("<h1> Update </h1>")


def login(request):
	return HttpResponse("<h1> Login </h1>")
