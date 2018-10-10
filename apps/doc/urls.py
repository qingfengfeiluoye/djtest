from django.urls import path
from . import views

app_name = "doc"
urlpatterns = [
    path('doc_download/', views.DocView.as_view(), name="doc_download"),
]
