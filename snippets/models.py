# snippets/models.py

from django.db import models
from django.contrib.auth.models import User

class Snippet(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_with = models.ManyToManyField(User, related_name='shared_snippets', blank=True)
    likes_count = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)

    def update_likes_count(self):
        self.likes_count = self.likes.count()
        self.save()

    def increment_views_count(self):
        self.views_count += 1
        self.save()
        
    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'snippet')
