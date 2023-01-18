from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QuizModel(models.Model):
    question = models.CharField(max_length=200,null=True)
    op1 = models.CharField(max_length=200,null=True)
    op2 = models.CharField(max_length=200,null=True)
    op3 = models.CharField(max_length=200,null=True)
    op4 = models.CharField(max_length=200,null=True)
    ans = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.question

class HangmanModel(models.Model):
    word = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.word

class HangmanGame(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    game_id = models.AutoField(primary_key=True)
    answer = models.CharField(max_length=20)
    guessed = models.CharField(max_length=10, default="")
    status = models.CharField(max_length=10, default="ongoing")

    def __unicode__(self):
        return "game is: " + self.answer + "written by " + self.user.first_name \
               + self.user.last_name