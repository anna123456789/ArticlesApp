from django.forms import ModelForm
from .models import Article, Author
from django.contrib.auth.models import User


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['author', 'like']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['user', 'text']
