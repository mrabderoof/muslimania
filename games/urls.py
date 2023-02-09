from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', games, name='games'),

    #Guess
    path('guess', guess_game, name="guess"),
    path('guess_name', guess_name, name="guess_name"),
    path('guess_names', guess_name, name="guess_names"),

    path('timed_guesses', timed_guesses, name="timed_guesses"),

    #Hangman
    path('hangman', start_game, name="hangman"),

    #Quiz
    path('quiz/', quiz,name='quiz'),

    #Create
    path('addGuess/', addGuess,name='addGuess'),
    path('addGuessName/', addGuessName,name='addGuessName'),
     path('addGuessNames/', addGuessName,name='addGuessNames'),
    path('addQuestion/', addQuestion,name='addQuestion'),
    path('addHangman/', addHangman,name='addHangman'),
    ]