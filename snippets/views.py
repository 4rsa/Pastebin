# snippets/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Snippet

# Create Snippet
@login_required
def create_snippet(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        Snippet.objects.create(title=title, content=content, user=request.user)
        return redirect('snippet_list')
    return render(request, 'snippets/create_snippet.html')

# List Snippets
@login_required
def snippet_list(request):
    snippets = Snippet.objects.filter(user=request.user)
    return render(request, 'snippets/snippet_list.html', {'snippets': snippets})

# Read Snippet
@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet})

# Update Snippet
@login_required
def update_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == 'POST':
        snippet.title = request.POST['title']
        snippet.content = request.POST['content']
        snippet.save()
        return redirect('snippet_detail', pk=snippet.pk)
    return render(request, 'snippets/update_snippet.html', {'snippet': snippet})

# Delete Snippet
@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    snippet.delete()
    return redirect('snippet_list')

# Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('snippet_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
