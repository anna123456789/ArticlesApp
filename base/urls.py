from django.urls import path, include
from . import views

#URLConf
urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('article/<str:pk>', views.article, name='article'),
    path('create-article/', views.createArticle, name='create-article'),
    path('update-article/<str:pk>/', views.updateArticle, name='update-article'),
    path('delete-article/<str:pk>/', views.deleteArticle, name='delete-article'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerPage, name='register'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment'),
    path('profile/<str:pk>/', views.profileUser, name='profile-user'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),
    path('', include('social_django.urls')),
]
