from django.db import models

class Users(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=30)

	def __unicode__(self):
		return self.username +' : ' + self.password
	