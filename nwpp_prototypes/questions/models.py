from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField
from django.utils.html import escape


def truncate(value):
    summary_size = 20
    if len(value) > summary_size:
        return '{0}...'.format(value[:summary_size])
    else:
        return value


class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    body = RichTextField()
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solved = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solution = models.BooleanField(default=False)
    vote_counter = models.IntegerField(default=0)

    def __str__(self):
        return f'RE: {self.question.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created} {self.answer}'


class Profile(models.Model):  # Extends base User class with additional fields
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="media/", blank=True, null=True)
    questions = models.IntegerField(default=0)
    answers = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    solutions = models.IntegerField(default=0)
    vote_counter = models.IntegerField(default=0)
    flags = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    searches = models.IntegerField(default=0)
    edits = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - Profile'


class Vote(models.Model):
    up = 'u'
    down = 'd'
    vote_types = (
        (up, 'Up voted'),
        (down, 'Down voted'),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    vote_type = models.CharField(max_length=1, choices=vote_types)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ('-date',)

    def __str__(self):
        if self.vote_type == self.up:
            return f'{self.user.username} voted up {self.answer}'
        else:
            return f'{self.user.username} voted down {self.answer}'


class Flag(models.Model):
    q = 'q'
    a = 'a'
    c = 'c'
    flag_types = (
        (q, 'Question'),
        (a, 'Answer'),
        (c, 'Comment'),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    comment = models.ForeignKey(Comment, null=True, blank=True)
    reason = models.CharField(max_length=200)
    # reason options are defined through a <select> tag on the front end in question_detail.html
    body = RichTextField()
    flag_type = models.CharField(max_length=1, choices=flag_types)

    class Meta:
        verbose_name = 'Flag'
        verbose_name_plural = 'Flags'
        ordering = ('-date',)

    def __str__(self):
        return truncate(self.body)


class Notification(models.Model):
    answered = 'a'
    solved = 's'
    voted = 'v'
    notification_types = (
        (answered, 'Answered'),
        (solved, 'Solved'),
        (voted, 'Voted')
        )

    answered_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> provided an answer to your question: <a href="/questions/question_detail/{2}">{3}</a></div>'
    solved_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> accepted your answer to the question: <a href="/questions/question_detail/{2}">{3}</a></div>'
    voted_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> voted for your answer to the question: <a href="/questions/question_detail/{2}">{3}</a></div>'

    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    notification_type = models.CharField(max_length=1, choices=notification_types)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.answered:
            return self.answered_template.format(
                escape(self.from_user.pk),
                escape(self.from_user.username),
                self.question.pk,
                escape(truncate(self.question.title))
                )
        elif self.notification_type == self.solved:
            return self.solved_template.format(
                escape(self.from_user.pk),
                escape(self.from_user.username),
                self.answer.question.pk,
                escape(truncate(self.answer.question.title))
                )
        elif self.notification_type == self.voted:
            return self.voted_template.format(
                escape(self.from_user.pk),
                escape(self.from_user.username),
                self.answer.question.pk,
                escape(truncate(self.answer.question.title))
                )
        else:
            return 'Ooops! Something went wrong.'


class Badge(models.Model):
    name = models.CharField(max_length=100)
    flavor_text = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="media/", blank=True, null=True)
    date_time = models.DateTimeField(auto_now=True)
    question_requirement = models.IntegerField(default=0)
    answer_requirement = models.IntegerField(default=0)
    vote_requirement = models.IntegerField(default=0)
    recipients = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

