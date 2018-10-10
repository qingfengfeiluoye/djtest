from django.urls import path
from . import views

# app_name 用于区分url的name
app_name = "news"
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('news_details/', views.NewsDetailsView.as_view(), name="news_details"),
    path('search/', views.SearchView.as_view(), name="search"),
]
