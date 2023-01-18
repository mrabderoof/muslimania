from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', games, name='games'),

    #Hangman
    path('hangman', start_game, name="hangman"),

    #Quiz
    path('quiz/', quiz,name='quiz'),
    path('addQuestion/', addQuestion,name='addQuestion'),
    path('addHangman/', addHangman,name='addHangman'),
    ]