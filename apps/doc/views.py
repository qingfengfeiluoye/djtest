from django.shortcuts import render
from django.views import View


class DocView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "doc/docDownload.html")
