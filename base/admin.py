from django.contrib import admin
from .models import Article, Topic, Author, Comment

# Register your models here.

admin.site.register(Article)
admin.site.register(Topic)
admin.site.register(Author)
admin.site.register(Comment)