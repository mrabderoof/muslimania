from django.contrib import admin

# Register your models here.
from .models import ProfileModel, LinkModel, bookmode

@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProfileModel._meta.fields]

@admin.register(LinkModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['link']


@admin.register(bookmode)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in bookmode._meta.fields]