from django.urls import path
from . import views

app_name = "admin"
urlpatterns = [
    path('index/', views.index, name="index"),
    path('new_tag_manage/', views.NewTagView.as_view(), name="new_tag_manage"),
    path('news_pub/', views.NewsPubView.as_view(), name="news_pub"),
    path('upload-file/', views.file_upload, name="upload-file"),
    path('up_token/', views.up_token, name="up_token"),
    path('news_manage/', views.NewsManageView.as_view(), name="news_manage"),

]
