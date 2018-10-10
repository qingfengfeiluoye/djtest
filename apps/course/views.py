from django.shortcuts import render
from django.views import View


class CourseView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "course/course.html")


class CourseDetailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "course/course_detail.html")
