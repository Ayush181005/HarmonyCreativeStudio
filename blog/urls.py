from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('oldestFirst', views.oldestFirst, name="oldestFirst"),
    path('most-popular', views.mostPopular, name="mostPopular"),
    path('search/', views.search, name='search'),

    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name="blogPost"),
]