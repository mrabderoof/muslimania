from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from .forms import *
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

# Django transaction system so we can use @transaction.atomic
from django.db import transaction
from .models import HangmanGame as Game

import random
from datetime import datetime
from random import choice
import logging
from django.contrib import messages


#List Games
def games(request):
    context = {}
    return render(request,'games/games.html',context)
    
#Hangman
logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('hangman')
logger.setLevel(logging.INFO)

@login_required
def start_game(request):
    if request.method == 'GET':
        words = HangmanModel.objects.all()
        if words.exists():
            word = str(random.choice(words)).lower()
        else:
            word = "muslimania"
        game = Game(user=request.user, answer=word)
        game.save()
        logger.info("starting new game %s for user:" % request.user)
        game.image = "/static/images/hang0.gif"
        game.display = "_ " * len(word)
        return render(request, "games/hangman/hangman.html", {'guessed': [], "game": game})
    else:
        return button(request)


def button(request):
    game_id = int(request.POST['game_id'])

    game = Game.objects.get(game_id=game_id)
    # avoid user change message
    if game.user != request.user:
        return render(request, "games/hangman/hangman.html")
    answer = game.answer

    cur_guess = request.POST['letter']
    guessed = list(game.guessed)

    if game.status == "win" or game.status == "lose":
        generate_finished_game(game)
        return render(request, "games/hangman/hangman.html", {'guessed': guessed, 'game': game})
    if cur_guess not in guessed:
        guessed.append(cur_guess)
        game.guessed = "".join(guessed)
        game.save()
    word_to_display = ""

    match_num = 0
    for char in answer:
        if char in guessed:
            match_num += 1
            word_to_display += char + ' '
        else:
            word_to_display += '_ '

    if match_num == len(answer):
        game.status = "win"
        game.save()
    game.display = word_to_display

    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 10:
        game.status = 'lose'
        game.save()
        num_wrong_guess = 10
    game.image = "/static/images/hang" + str(num_wrong_guess) + ".gif"

    return render(request, "games/hangman/hangman.html", {'guessed': guessed, 'game': game})


def generate_finished_game(game):
    answer = game.answer
    guessed = list(game.guessed)
    if game.status == "win":
        game.display = " ".join(list(answer))
        game.image = "/static/images/hang" + str(wrong_num(guessed, answer)) + ".gif"
        return
    else:
        game.display = word_to_display(guessed, answer)
        game.image = "/static/images/hang10.gif"
        return


def wrong_num(guessed, answer):
    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 10:
        num_wrong_guess = 10
    return num_wrong_guess


def word_to_display(guessed, answer):
    display = ""
    match_num = 0
    for char in answer:
        if char in guessed:
            match_num += 1
            display += char + " "
        else:
            display += '_ '
    return display


# Quiz Game
def quiz(request):
    if request.method == 'POST':
        print(request.POST)
        questions=QuizModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        percent = score/(total*10) *100
        context = {
            'score':score,
            'time': request.POST.get('timer'),
            'correct':correct,
            'wrong':wrong,
            'percent':percent,
            'total':total
        }
        return render(request,'games/quiz/result.html',context)
    else:
        questions=QuizModel.objects.all()
        context = {
            'questions':questions
        }
        return render(request,'games/quiz/quiz.html',context)
 
@login_required
def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                next = request.POST.get("next", "/")
                return HttpResponseRedirect(next)
        context={'form':form}
        return render(request,'games/quiz/add_question.html',context)
    else: 
        return redirect('/users/login/') 
 

@login_required
def addHangman(request):    
    if request.user.is_staff:
        form=addHangmanform()
        if(request.method=='POST'):
            form=addHangmanform(request.POST)
            if(form.is_valid()):
                form.save()
                next = request.POST.get("next", "/")
                return HttpResponseRedirect(next)
        context={'form':form}
        return render(request,'games/quiz/add_question.html',context)
    else: 
        return redirect('/users/login/') 