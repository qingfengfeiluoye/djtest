from django.urls import path
from . import views

# app_name 用于区分url的name
app_name = "news"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('news/details/<int:news_id>', views.news_details, name="news_details"),
    path('news/add_comment/', views.NewsAddComments.as_view(), name="news_add_comment"),
    path('news/comment/', views.news_comments, name="news_comments"),
    path('news/list/', views.news_list, name="news_list"),
    path('search/', views.SearchView.as_view(), name="search"),
]
