from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/index.html")


class NewsDetailsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/news_detail.html")


class SearchView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/search.html")
