# snippets/templatetags/custom_filters.py
from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def time_ago(value):
    now = timezone.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff < timedelta(days=7):
        days = int(diff.total_seconds() / 86400)
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif diff < timedelta(weeks=4):
        weeks = int(diff.total_seconds() / 604800)
        return f"{weeks} week{'s' if weeks > 1 else ''} ago"
    elif diff < timedelta(days=365):
        months = int(diff.total_seconds() / 2592000)
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = int(diff.total_seconds() / 31536000)
        return f"{years} year{'s' if years > 1 else ''} ago"
