from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    tags = TaggableManager()
    date_time = models.DateTimeField(auto_now=True)
    solved = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

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


class Profile(models.Model):  # Extends base User class with additional fields
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="questions/media/", blank=True, null=True)
    questions = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    solutions = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - Profile'


