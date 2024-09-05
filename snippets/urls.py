# snippets/urls.py
from django.urls import path
from .views import my_snippets, all_snippets, create_snippet, snippet_detail, update_snippet, delete_snippet, share_snippet

urlpatterns = [
    path('my-snippets/', my_snippets, name='my_snippets'),
    path('all-snippets/', all_snippets, name='all_snippets'),
    path('create/', create_snippet, name='create_snippet'),
    path('<int:pk>/', snippet_detail, name='snippet_detail'),
    path('<int:pk>/update/', update_snippet, name='update_snippet'),
    path('<int:pk>/delete/', delete_snippet, name='delete_snippet'),
    path('<int:pk>/share/', share_snippet, name='share_snippet'),  # Add this line for sharing
]


