from django.urls import path
from . import views

app_name = "account"
urlpatterns = [
   path('login/', views.LoginView.as_view(), name="login"),
   path('logout/', views.logout_view, name="logout"),
   path('register/', views.RegisterView.as_view(), name="register"),
   path('make_captcha/', views.make_captcha, name="make_captcha"),
   path('send_message/', views.send_message, name="send_message"),
   path('change_password/', views.ChangPassword.as_view(), name="change_password"),
]
