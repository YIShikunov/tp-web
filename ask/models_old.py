import datetime
from django.db import models
from django.contrib.auth.models import User

class tag(models.Model):
	tagline = models.CharField(max_length=255)

	def __unicode__(self):
		return self.tagline
	      
	      
class question(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(default=datetime.datetime.now)
	tags = models.ManyToManyField(tag)

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return '/post/%d/' % self.pk

	class Meta:
		ordering = ['-creation_date']

class answer(models.Model):
	content = models.TextField()
	author = models.ForeignKey(User)
	creation_date = models.DateTimeField(default=datetime.datetime.now)
	correct = models.BooleanField(default=False)
	quest = models.ForeignKey(question)

class user_data(models.Model):
	avatar = models.ImageField(upload_to='avatars')
	rating = models.IntegerField()
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return self.user.username
