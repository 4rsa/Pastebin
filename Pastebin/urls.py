# Pastebin/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('snippets/', include('snippets.urls')),  # Include your app URLs here
]
