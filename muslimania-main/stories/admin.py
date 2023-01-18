from django.contrib import admin

# Register your models here.
from .models import Book, Author, Publisher, Story

@admin.register(Book)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'publisher']

@admin.register(Author)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Author._meta.fields]

@admin.register(Publisher)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Publisher._meta.fields]

@admin.register(Story)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['chapter_no']
