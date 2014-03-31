from django.conf.urls import patterns, url

from syncfolder import views

urlpatterns = patterns('',

	url(r'^$', views.index, name='index'),
	url(r'^send$', views.send, name='send'),
	url(r'^remove$', views.remove, name='remove'),
	url(r'^update$', views.update, name='update'),
)