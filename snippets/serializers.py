# snippets/serializers.py

from rest_framework import serializers
from .models import Snippet

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user']
        read_only_fields = ['user']
