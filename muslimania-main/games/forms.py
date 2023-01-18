from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

 
class addQuestionform(ModelForm):
    class Meta:
        model=QuizModel
        fields="__all__"

class addHangmanform(ModelForm):
    class Meta:
        model=HangmanModel
        fields="__all__"
