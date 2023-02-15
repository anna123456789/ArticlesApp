from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from .models import Article, Topic, Author, Comment
from .forms import ArticleForm, UserForm, AuthorForm

# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    all_articles = Article.objects.all()
    articles = Article.objects.filter(Q(topic__name__icontains=q) | Q(text__icontains=q) | Q(name__icontains=q))
    article_count = articles.count()

    topics = Topic.objects.all()[0:5]
    # article_comments=Comment.objects.filter(Q(article__topic__name__icontains=q))

    if request.user.is_authenticated:
        # article_comments = Comment.objects.filter(Q(article__author__subscribers=request.user) | Q(article__likes=request.user))
        subscribed_authors = Author.objects.filter(Q(subscribers=request.user))
        article_comments = Comment.objects.filter(Q(article__likes=request.user))
        for subscribed_author in subscribed_authors:
            article_comments = article_comments | Comment.objects.filter(Q(user=subscribed_author.user))
        article_comments = article_comments.distinct()
    else:
        article_comments = {}

    context = {'articles': articles, 'topics': topics, 'article_count': article_count,
               'article_comments': article_comments, 'all_articles': all_articles}
    return render(request, 'base/home.html', context)


def article(request, pk):
    page = 'article'
    article = Article.objects.get(id=pk)
    comments = article.comment_set.all()
    likes = article.likes.all()

    if request.method == "POST":
        if 'like' in request.POST:
            if request.user.is_authenticated:
                article.likes.add(request.user)
            else:
                # return redirect('login')
                return redirect('/login/auth0')
        else:
            if 'unlike' in request.POST:
                if request.user.is_authenticated:
                    article.likes.remove(request.user)
                else:
                    # return redirect('login')
                    return redirect('/login/auth0')
            else:
                comment = Comment.objects.create(
                    user=request.user,
                    article=article,
                    text=request.POST.get('text')
                )
                return redirect('article', pk=article.id)

    context = {'article': article, 'comments': comments, 'users': likes, 'page': page}
    return render(request, 'base/article.html', context)


# @login_required(login_url='login')
@login_required(login_url='/login/auth0')
def createArticle(request):
    form = ArticleForm()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        author, created = Author.objects.get_or_create(user=request.user)
        Article.objects.create(
            author=author,
            name=request.POST.get('name'),
            topic=topic,
            text=request.POST.get('text')
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/article_form.html', context)


# @login_required(login_url='login')
@login_required(login_url='/login/auth0')
def updateArticle(request, pk):
    article = Article.objects.get(id=pk)
    form = ArticleForm(instance=article)
    topics = Topic.objects.all()

    if request.user != article.author.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        article.name = request.POST.get('name')
        article.topic = topic
        article.text = request.POST.get('text')
        article.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'article': article}
    return render(request, 'base/article_form.html', context)


# @login_required(login_url='login')
@login_required(login_url='/login/auth0')
def deleteArticle(request, pk):
    article = Article.objects.get(id=pk)

    if request.user != article.author.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        article.delete()
        return redirect('home')

    context = {'obj': article, 'obj_type': 'an ' + Article.__name__.lower()}
    return render(request, 'base/delete.html', context)


# @login_required(login_url='login')
@login_required(login_url='/login/auth0')
def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user:
        return HttpResponse("You are not allowed here")

    if request.method == "POST":
        comment.delete()
        return redirect('home')

    context = {'obj': comment, 'obj_type': 'a ' + Comment.__name__.lower()}
    return render(request, 'base/delete.html', context)


def logoutUser(request):
    logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000/articles/home'  # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')
    # return redirect('home')


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User don't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def registerPage(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Author.objects.create(
                user=user
            )
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")

    form = UserCreationForm()

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def profileUser(request, pk):
    all_articles = Article.objects.all()
    user = User.objects.get(id=pk)
    author = Author.objects.get(user=user)
    articles = author.article_set.all()
    comments = user.comment_set.all()
    topics = Topic.objects.all()
    users = author.subscribers.all()

    if request.method == "POST":
        if 'subscribe' in request.POST:
            if request.user.is_authenticated:
                author.subscribers.add(request.user)
            else:
                # return redirect('login')
                return redirect('/login/auth0')
        else:
            if 'unsubscribe' in request.POST:
                if request.user.is_authenticated:
                    author.subscribers.remove(request.user)
                else:
                    # return redirect('login')
                    return redirect('/login/auth0')

    context = {'user': user, 'users': users, 'author': author, 'articles': articles, 'comments': comments,
               'topics': topics, 'all_articles': all_articles}
    return render(request, 'base/profile.html', context)


# @login_required(login_url='login')
@login_required(login_url='/login/auth0')
def updateUser(request):
    user = request.user
    author, created = Author.objects.get_or_create(
        user=user
    )
    # author = Author.objects.get(user=user)
    form = UserForm(instance=user)
    if request.method == "POST":
        # form = UserForm(request.POST, instance=user)
        # if form.is_valid():
        #     form.save()

        author.user.username = request.POST.get('username')
        author.user.email = request.POST.get('email')
        author.text = request.POST.get('text')
        author.save()
        return redirect('home')
        # return redirect('profile-user', pk = user.id)

    context = {'form': form, 'author': author}
    return render(request, 'base/update-user.html', context)


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activityPage(request):
    # comments=Comment.objects.all()
    if request.user.is_authenticated:
        comments = Comment.objects.filter(Q(article__author__subscribers=request.user) | Q(article__likes=request.user))
    else:
        comments = {}
    context = {'comments': comments}
    return render(request, 'base/activity.html', context)


