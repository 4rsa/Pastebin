# Generated by Django 4.2.11 on 2024-09-05 15:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snippets', '0006_remove_snippet_content_snippet_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='shared_with',
            field=models.ManyToManyField(blank=True, related_name='shared_snippets', to=settings.AUTH_USER_MODEL),
        ),
    ]
