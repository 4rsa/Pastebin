# Generated by Django 4.2.11 on 2024-08-27 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='code',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='snippet',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
