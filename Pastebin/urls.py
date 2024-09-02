# Pastebin/urls.py

from django.contrib import admin
from django.urls import path, include
from snippets.views import register

urlpatterns = [
    path('admin/', admin.site.urls),
    path('snippets/', include('snippets.urls')),  # Include your app URLs here
    path('accounts/', include('django.contrib.auth.urls')),  # Add this line
    path('register/', register, name='register'),

]