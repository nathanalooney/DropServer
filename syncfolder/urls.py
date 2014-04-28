from django.conf.urls import patterns, url

from syncfolder import views

urlpatterns = patterns('',

	url(r'^$', views.index, name='index'),
	url(r'^fileCreate$', views.fileCreate, name='fileCreate'),
	url(r'^dirCreate$', views.dirCreate, name='dirCreate'),
	url(r'^fileDelete$', views.fileDelete, name = 'fileDelete'),
	url(r'^dirDelete$', views.dirDelete, name='dirDelete'),
	url(r'^update$', views.update, name='update'),
	url(r'^move$', views.move, name='move'),
	url(r'^pull$', views.pull, name='pull'),
	url(r'^getServerIndex$', views.getServerIndex, name='getServerIndex'),
	url(r'^setup$', views.setup, name='setup'),
	url(r'^login$', views.login, name='login'),
)
