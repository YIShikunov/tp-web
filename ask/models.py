from django.db import models
#from django import utils
import datetime
from django.contrib.auth.models import User
# Create your models here.

class UserAccount(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to = 'avatars')
    rating = models.IntegerField()
    def __unicode__(self):
	return self.user

class Tag(models.Model):
	tagName = models.CharField(max_length = 80)
	def __unicode__(self):
		return self.tagName
class Question(models.Model):
	name = models.CharField(max_length = 140)
	content = models.TextField()
	author = models.ForeignKey(UserAccount)
	creationDate = models.DateTimeField(default = datetime.datetime.utcnow)
	tags = models.ManyToManyField(Tag)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ['-creationDate']

class Answer(models.Model):
	content = models.TextField()
	author = models.ForeignKey(UserAccount)
	creationDate = models.DateTimeField(default= datetime.datetime.utcnow)
	approved = models.BooleanField(default=False)
	question = models.ForeignKey(Question)

	def __unicode__(self):
		return self.question +' answered by ' + self.author
