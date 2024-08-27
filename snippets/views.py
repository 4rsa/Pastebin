# snippets/views.py

from django.shortcuts import render
from .models import Snippet

def snippet_list(request):
    snippets = Snippet.objects.all()
    return render(request, 'snippets/snippet_list.html', {'snippets': snippets})
