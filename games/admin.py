from django.contrib import admin
from .models import QuizModel, HangmanModel

# Register your models here.
admin.site.register(HangmanModel)

@admin.register(QuizModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in QuizModel._meta.fields]
