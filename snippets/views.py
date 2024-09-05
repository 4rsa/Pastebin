# snippets/views.py

import boto3
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Snippet
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

# Create Snippet
@login_required
def create_snippet(request):
    next_url = request.GET.get('next', 'all_snippets')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f'snippets/{title}.txt',
            Body=content
        )
        url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/snippets/{title}.txt'
        Snippet.objects.create(title=title, url=url, user=request.user)
        return redirect(next_url)  # Redirect to next_url
    return render(request, 'snippets/create_snippet.html', {'next': next_url})


# Read Snippet
@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    # Download content from S3
    response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=snippet.url.split(f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')[1])
    content = response['Body'].read().decode('utf-8')
    return render(request, 'snippets/snippet_detail.html', {'snippet': snippet, 'content': content})

# Update Snippet
@login_required
def update_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    
    if snippet.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this snippet.")

    next_url = request.GET.get('next', f'snippet_detail/{snippet.pk}')  # Default to snippet detail if no next param

    if request.method == 'POST':
        snippet.title = request.POST['title']
        content = request.POST['content']
        s3_client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=f'snippets/{snippet.title}.txt',
            Body=content
        )
        snippet.url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/snippets/{snippet.title}.txt'
        snippet.save()
        return redirect(next_url)  # Redirect to next_url
    return render(request, 'snippets/update_snippet.html', {'snippet': snippet, 'next': next_url})


# Delete Snippet
@login_required
def delete_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    s3_client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=snippet.url.split(f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/')[1])
    snippet.delete()
    next_url = request.GET.get('next', 'all_snippets')  # Default to 'all_snippets' if no next param
    return redirect(next_url)


# List Snippets
@login_required
def my_snippets(request):
    user = request.user
    snippets = Snippet.objects.filter(user=user)
    shared_snippets = Snippet.objects.filter(shared_with=user)
    return render(request, 'snippets/my_snippets.html', {'my_snippets': snippets, 'shared_snippets': shared_snippets})

def all_snippets(request):
    snippets = Snippet.objects.all()  # Get all snippets, regardless of the user
    return render(request, 'snippets/all_snippets.html', {'snippets': snippets})

@login_required
def share_snippet(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    
    if request.method == 'POST':
        shared_with = request.POST['shared_with'].split(',')
        recipients = User.objects.filter(username__in=shared_with)
        
        # Check for users that don't exist
        non_existent_users = set(shared_with) - set(recipients.values_list('username', flat=True))
        
        if non_existent_users:
            # Add an error message for non-existent users
            messages.error(request, f"The following users do not exist: {', '.join(non_existent_users)}")
        else:
            # Share the snippet with valid recipients
            snippet.shared_with.set(recipients)
            snippet.save()
            messages.success(request, "Snippet shared successfully.")
            return redirect('my_snippets')

    return render(request, 'snippets/share_snippet.html', {'snippet': snippet})

# Register
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