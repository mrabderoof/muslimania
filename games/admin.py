from django.contrib import admin
from .models import QuizModel, HangmanModel, NameModel, NamesModel, logName

# Register your models here.
admin.site.register(HangmanModel)
admin.site.register(NameModel)
admin.site.register(NamesModel)
admin.site.register(logName)

@admin.register(QuizModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [f.name for f in QuizModel._meta.fields]
