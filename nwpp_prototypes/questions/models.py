from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = RichTextField()
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solved = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


# class Vote(models.Model):
#     pass


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solution = models.BooleanField(default=False)
    vote_counter = models.IntegerField(default=0)
    # votes = models.ManyToManyField(Vote)

    def __str__(self):
        return f'RE: {self.question.title}'


class Profile(models.Model):  # Extends base User class with additional fields
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="questions/media/", blank=True, null=True)
    questions = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    solutions = models.IntegerField(default=0)
    vote_counter = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - Profile'


# class Notification(models.Model):
#     date_time = models.DateTimeField(auto_now=True)
#     activator = models.ForeignKey(User, on_delete=models.CASCADE)
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
#     solution = models.BooleanField(default=False)
#     vote = models.BooleanField(default=False)


class Badge(models.Model):
    name = models.CharField(max_length=100)
    flavor_text = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="questions/media/", blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    question_requirement = models.IntegerField(default=0)
    answer_requirement = models.IntegerField(default=0)
    vote_requirement = models.IntegerField(default=0)
    recipients = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

