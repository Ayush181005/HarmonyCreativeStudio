from django.urls import path
from blog import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('oldestFirst', views.oldestFirst, name="oldestFirst"),
    path('most-popular', views.mostPopular, name="mostPopular"),
    path('search/', views.search, name='search'),

    path('', views.blogHome, name='blogHome'),
    path('post/<str:slug>', views.blogPost, name="blogPost"),
]