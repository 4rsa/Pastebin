# snippets/models.py

from django.db import models

class Snippet(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # This field should be here
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
