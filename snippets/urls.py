# snippets/urls.py
from django.urls import path
from .views import snippet_list

urlpatterns = [
    path('', snippet_list, name='snippet_list'),
]
