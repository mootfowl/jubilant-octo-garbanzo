from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    solution = models.BooleanField(default=False)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'RE: {self.question.title}'
