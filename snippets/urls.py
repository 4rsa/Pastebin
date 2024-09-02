# snippets/urls.py
from django.urls import path
from .views import create_snippet, snippet_list, snippet_detail, update_snippet, delete_snippet
from rest_framework.authtoken.views import obtain_auth_token  # Import obtain_auth_token view

urlpatterns = [
    path('', snippet_list, name='snippet_list'),
    path('create/', create_snippet, name='create_snippet'),
    path('<int:pk>/', snippet_detail, name='snippet_detail'),
    path('<int:pk>/update/', update_snippet, name='update_snippet'),
    path('<int:pk>/delete/', delete_snippet, name='delete_snippet'),
]

