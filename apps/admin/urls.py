from django.urls import path
from . import views

app_name = "admin"
urlpatterns = [
    path('index/', views.index, name="index"),

]
