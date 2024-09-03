# snippets/models.py

from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()  # Changed from content to url
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
