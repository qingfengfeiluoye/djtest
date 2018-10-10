from django.urls import path
from . import views

app_name = "course"
urlpatterns = [
    path('course/', views.CourseView.as_view(), name="course"),
    path('course_detail/', views.CourseDetailView.as_view(), name="course_detail"),
]
