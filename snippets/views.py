# snippets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import boto3

from .models import Snippet, Like

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

# Snippet CRUD Operations

@login_required
def create_snippet(request):
    next_url = request.GET.get('next', 'all_snippets')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        s3_key = f'snippets/{title}.txt'
        
        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                Body=content
            )
        except Exception as e:
            messages.error(request, f"Failed to upload snippet: {str(e)}")
            return redirect('create_snippet')

        url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}'
        Snippet.objects.create(title=title, url=url, user=request.user)
        return redirect(next_url)
    
    return render(request, 'snippets/create_snippet.html', {'next': next_url})


@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    snippet.increment_views_count()
    s3_key = snippet.url.split(f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')[1]

    try:
        response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        content = response['Body'].read().decode('utf-8')
    except Exception as e:
        messages.error(request, f"Failed to retrieve snippet: {str(e)}")
        return redirect('all_snippets')

    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet, 'content': content})


@login_required
def update_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if snippet.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this snippet.")

    next_url = request.GET.get('next', f'snippet_detail/{snippet.pk}')

    # Retrieve the content from S3
    s3_key = f'snippets/{snippet.title}.txt'
    try:
        s3_object = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
        content = s3_object['Body'].read().decode('utf-8')
    except Exception as e:
        messages.error(request, f"Failed to retrieve snippet content: {str(e)}")
        content = ''  # Default to empty content if retrieval fails

    if request.method == 'POST':
        snippet.title = request.POST['title']
        content = request.POST['content']
        s3_key = f'snippets/{snippet.title}.txt'

        try:
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=s3_key,
                Body=content
            )
        except Exception as e:
            messages.error(request, f"Failed to update snippet: {str(e)}")
            return redirect('update_snippet', pk=pk)

        snippet.url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}'
        snippet.save()
        return redirect(next_url)
    
    # Pass the content to the template
    return render(request, 'snippets/update_snippet.html', {'snippet': snippet, 'content': content, 'next': next_url})


@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    s3_key = snippet.url.split(f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')[1]

    try:
        s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key)
    except Exception as e:
        messages.error(request, f"Failed to delete snippet: {str(e)}")
        return redirect('my_snippets')

    snippet.delete()
    next_url = request.GET.get('next', 'all_snippets')
    return redirect(next_url)

@login_required
def like_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    if request.method == 'POST':
        like, created = Like.objects.get_or_create(snippet=snippet, user=request.user)
        
        if not created:
            like.delete()
        
        snippet.update_likes_count()
        
        # Debugging log
        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f"Likes count for snippet {pk}: {snippet.likes_count}")
        
        # Return JSON response
        return JsonResponse({
            'likes_count': snippet.likes_count,
            'liked': created
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def share_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)

    if request.method == 'POST':
        shared_with = request.POST['shared_with'].split(',')
        recipients = User.objects.filter(username__in=shared_with)
        
        non_existent_users = set(shared_with) - set(recipients.values_list('username', flat=True))
        
        if non_existent_users:
            messages.error(request, f"The following users do not exist: {', '.join(non_existent_users)}")
        else:
            snippet.shared_with.set(recipients)
            snippet.save()
            messages.success(request, "Snippet shared successfully.")
            return redirect('my_snippets')

    return render(request, 'snippets/share_snippet.html', {'snippet': snippet})


# Snippet Listing Views

@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    shared_snippets = Snippet.objects.filter(shared_with=request.user)
    return render(request, 'snippets/my_snippets.html', {'my_snippets': snippets, 'shared_snippets': shared_snippets})

def all_snippets(request):
    sort_by = request.GET.get('sort_by', 'created_at')
    
    if sort_by == 'likes':
        snippets = Snippet.objects.all().order_by('-likes_count')
    elif sort_by == 'alphabet':
        snippets = Snippet.objects.all().order_by('title')
    elif sort_by == 'views':
        snippets = Snippet.objects.all().order_by('-views_count')  # Fixed line
    else:
        snippets = Snippet.objects.all().order_by('-created_at')
    
    context = {
        'snippets': snippets,
    }
    return render(request, 'snippets/all_snippets.html', context)


# User Registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('all_snippets')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})