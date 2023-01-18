# Generated by Django 4.1 on 2022-08-29 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_rename_story_story_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='book',
        ),
        migrations.AddField(
            model_name='story',
            name='book',
            field=models.ManyToManyField(blank=True, to='stories.book'),
        ),
    ]