# snippets/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Snippet
from django.http import HttpResponse

# Create Snippet
def create_snippet(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        
        # Save Snippet to the database
        Snippet.objects.create(title=title, content=content)
        return redirect('snippet_list')
    
    return render(request, 'snippets/create_snippet.html')

# List Snippets
def snippet_list(request):
    snippets = Snippet.objects.all()
    return render(request, 'snippets/snippet_list.html', {'snippets': snippets})

# Read Snippet
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

# Update Snippet
def update_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == 'POST':
        snippet.title = request.POST['title']
        snippet.content = request.POST['content']
        snippet.save()
        return redirect('snippet_detail', pk=snippet.pk)
    
    return render(request, 'snippets/update_snippet.html', {'snippet': snippet})

# Delete Snippet
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    snippet.delete()
    return redirect('snippet_list')
