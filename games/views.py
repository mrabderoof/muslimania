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

from django.views.decorators.csrf import csrf_exempt
from random import randint

#List Games
def games(request):
    context = {}
    return render(request,'games/games.html',context)

def timed_guesses(request):
    context = {}
    return render(request,'games/games.html',context)

names_list = NamesModel.objects.all()
def get_name():
    if names_list.exists():
        ran = random.randint(0, names_list.count()-1)
        name_list = names_list[ran].name
        hints = names_list[ran].hint
        length = len(name_list)
    else:
        name_list = "Mohammad"
        hints = "SAW"
        length = 8
    name = [name_list, hints, length]
    return name

name = get_name()
secret_name = name[0]
hints = name[1]
length = name[2]
turn = 0
success = False

#Incrementor

def Incrementor(request, game, win):
    b = logName.objects.filter(user=request.user).filter(games=game)
    flag = 0
    if b.exists():
        flag = 1
        for bb in b:
            if bb.turns == turn:
                if win ==1:
                    bb.wins = bb.wins+1
                bb.gp = bb.gp+1
                bb.turns = bb.turns + turn
                bb.save()
                flag = 1
                break
            else:
                flag = 0
    if flag == 0:
        f = logName(user=request.user, games=game, turns=turn, wins=win, gp=1)
        f.save()

# def Incrementor(request, game, win):
#     b = logName.objects.filter(user=request.user).filter(games=game)
#     if b.exists():
#         for bb in b:
#             if win ==1:
#                 bb.wins = bb.wins+1
#             bb.gp = bb.gp+1
#             bb.turns = bb.turns + turn
#             bb.save()
#     else:
#         f = logName(user=request.user, games=game, turns=turn, wins=win, gp=1)
#         f.save()

#Guess name/prophet, surah, Juz, Prophet
@csrf_exempt
def guess_name(request):
    global secret_name, turn, success, hints, length
    context = {}
    hint = ''
    guessed_name = None
    if request.method == 'POST' and request.POST.get('guess_name'):
        guessed_name = str(request.POST['guess_name'])
        turn +=1
        if guessed_name.lower() == secret_name.lower():
            success = True
            if request.user.is_authenticated:
                Incrementor(request, "names", 1)
        else:
            hint = 'not quite'
        
    else:
        name = get_name()
        secret_name = name[0]
        hints = name[1]
        length = name[2]
        turn = 0
        success = False
        hint = ''
        guessed_name = None
    
    context = {
        "length": length, 'hints': hints,
        'success': success, 'turn': turn,
        'hint': hint,'guessed_name': guessed_name
        }
    return render(request, 'games/guess/name.html', context)

secret_number = randint(0, 100)

#Guess number
@csrf_exempt
def guess_game(request):
    global secret_number, turn, success
    context = {}
    hint = ''
    guessed_number = None

    if request.method == 'POST' and request.POST.get('guess_number'):
        guessed_number = int(request.POST['guess_number'])
        turn +=1
        if guessed_number == secret_number:
            success = True
            if request.user.is_authenticated:
                Incrementor(request, "numbers", 1)
        else:
            if(guessed_number > secret_number):
                hint = 'lower'
            else:
                hint = 'higher'
        
    else:
        secret_number = randint(0,100)
        turn = 0
        success = False
        hint = ''
        guessed_number = None
    
    context = {
        'success': success, 'turn': turn,
        'hint': hint,'guessed_number': guessed_number
        }
    return render(request, 'games/guess/guess_game.html', context)

#Hangman
logger_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logger_format)
logger = logging.getLogger('hangman')
logger.setLevel(logging.INFO)

#Hangman
def start_game(request):
    if request.method == 'GET':
        words = HangmanModel.objects.all()
        if words.exists():
            word = str(random.choice(words)).lower()
        else:
            word = "muslimania"
        
        if request.user.is_authenticated:
            game = Game(user=request.user, answer=word)
            game.save()
            logger.info("starting new game %s for user:" % request.user)
        else:
            game = Game(answer=word)
            game.save()
            logger.info("starting new game:")
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
        generate_finished_game(game, request)
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
        if request.user.is_authenticated:
            Incrementor(request, "hangman", 1)
        game.save()
    game.display = word_to_display

    num_wrong_guess = 0
    for char in guessed:
        if char not in answer:
            num_wrong_guess += 1
    if num_wrong_guess >= 7:
        game.status = 'lose'
        if request.user.is_authenticated:
            Incrementor(request, "hangman", 0)
        game.save()
        num_wrong_guess = 7
    game.image = "/static/images/hang" + str(num_wrong_guess) + ".gif"

    return render(request, "games/hangman/hangman.html", {'guessed': guessed, 'game': game})


def generate_finished_game(game, request):
    global turn
    answer = game.answer
    guessed = list(game.guessed)
    if game.status == "win":
        game.display = " ".join(list(answer))
        game.image = "/static/images/hang" + str(turn) + ".gif"
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
    if num_wrong_guess >= 7:
        num_wrong_guess = 7
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
        questions=QuizModel.objects.all()
        score=0
        wrong=0
        correct=0
        total=0
        for q in questions:
            total+=1
            if q.ans ==  request.POST.get(q.question):
                score+=10
                correct+=1
            else:
                wrong+=1
        
        percent = score/(total*10) *100
        print(percent)
        if percent >= 50.0:
            Incrementor(request, "quiz", 1)
        else:
            Incrementor(request, "quiz", 0)
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
 


#Creat Guess
@login_required
def addGuess(request):    
    if request.user.is_authenticated:
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

@login_required
def addGuessName(request):    
    if request.user.is_authenticated:
        form=guessNameAddForm()
        if(request.method=='POST'):
            form=guessNameAddForm(request.POST)
            if(form.is_valid()):
                form.save()
                next = request.POST.get("next", "/")
                return HttpResponseRedirect(next)
        context={'form':form}
        return render(request,'games/quiz/add_question.html',context)
    else: 
        return redirect('/users/login/') 

@login_required
def addQuestion(request):    
    if request.user.is_authenticated:
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
    if request.user.is_authenticated:
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

