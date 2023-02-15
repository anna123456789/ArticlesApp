from django.db import models
from django.contrib.auth.models import User
#from django.db.models.deletion import CASCADE


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
        return self.name

class Author(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete = models.CASCADE)    #data of author: username, password, email etc.
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank = True)             #users who subscribe the author
    text = models.CharField(max_length=1000, blank=True, null=True)                                                         #description of author

    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.user)

class Article(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length=200)
    text = models.TextField(null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank = True)  #users who gave a like
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.text[0:50]