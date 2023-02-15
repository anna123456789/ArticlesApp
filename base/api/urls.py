from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoute),
    path('articles/', views.getArticles),
    path('articles/<str:pk>/', views.getArticle),
]