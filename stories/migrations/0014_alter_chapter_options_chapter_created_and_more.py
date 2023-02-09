# Generated by Django 4.0.7 on 2023-02-01 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0013_title_chapter'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ('created',)},
        ),
        migrations.AddField(
            model_name='chapter',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
