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


class Icon(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'<span class="fa fa-{self.name}"></span>'


class Category(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def icon(self):  # This is...clunky, and hard-coded (and thus limiting). But it works...
        if self.title == 'Fundamentals':
            return '<span class="fa fa-th-large"></span> FUNDAMENTALS | '
        elif self.title == 'Operations':
            return '<span class="fa fa-cog"></span> OPERATIONS | '
        elif self.title == 'Planning':
            return '<span class="fa fa-line-chart"></span> PLANNING | '


class Hive(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    icon = models.ForeignKey(Icon, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    # colorField??

    class Meta:
        verbose_name = 'Hive'
        verbose_name_plural = 'Hives'
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Invite(models.Model):
    hive = models.ForeignKey(Hive, null=True, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pass


class Question(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    hive = models.ForeignKey(Hive, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    body = RichTextField()
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    solved = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def bookmark_check(self, user):
        bookmark_ids = []
        for bookmark in user.bookmark_set.all():
            bookmark_ids.append(bookmark.question.id)
        # print(bookmark_ids)
        # print(self.id)
        return self.id in bookmark_ids


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

    def voters(self):
        voters = []
        for vote in self.vote_set.all():
            voters.append(vote.user)
        return voters

    def flaggers(self):
        flaggers = []
        for flag in self.flag_set.all():
            flaggers.append(flag.user)
        return flaggers


class Comment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    body = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.created} {self.answer}'


class Profile(models.Model):  # Extends base User class with additional fields
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    hives = models.ManyToManyField(Hive, blank=True)
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
    bookmarks = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} - Profile'

    def earned_badges(self):
        badges = []
        for badge in self.user.badge_set.all():
            badges.append(badge)
        return badges


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
    flag_type = models.CharField(max_length=1, choices=flag_types)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True)
    answer = models.ForeignKey(Answer, null=True, blank=True)
    comment = models.ForeignKey(Comment, null=True, blank=True)
    reason = models.CharField(max_length=200)
    # reason options are defined through a <select> tag on the front end in question_detail.html
    body = models.TextField()

    class Meta:
        verbose_name = 'Flag'
        verbose_name_plural = 'Flags'
        ordering = ('-date',)

    def __str__(self):
        return truncate(self.body)


class Bookmark(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True)
    note = models.TextField(null=True, blank=True)  # 2018.01.04 - NYI, presently no way leaving a note on front end

    class Meta:
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.user.username} bookmarked Question {self.question.id}'


class Notification(models.Model):
    answered = 'a'
    solved = 's'
    voted = 'v'
    flagged = 'f'
    notification_types = (
        (answered, 'Answered'),
        (solved, 'Solved'),
        (voted, 'Voted'),
        (flagged, 'Flagged')
        )

    answered_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> provided an answer to your question: <a href="/questions/question_detail/{2}">{3}</a></div>'
    solved_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> accepted your answer to the question: <a href="/questions/question_detail/{2}">{3}</a></div>'
    voted_template = '<div class="notification_message"><a href="/questions/profile/{0}">{1}</a> voted for your answer to the question: <a href="/questions/question_detail/{2}">{3}</a></div>'
    flagged_template = '<div class="notification_message"><a href="/questions/question_detail/{0}">Your post</a> was flagged {1} for the following reason: <i>"{2}"</i></div>'

    from_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
    flag = models.ForeignKey(Flag, null=True, blank=True, on_delete=models.CASCADE)
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
        elif self.notification_type == self.flagged:
            return self.flagged_template.format(
                escape(self.flag.answer.question.id),
                escape(self.flag.reason),
                escape(self.flag.body)
                )
        else:
            return 'Ooops! Something went wrong.'


class Badge(models.Model):
    name = models.CharField(max_length=100)
    flavor_text = models.CharField(max_length=100)
    icon = models.CharField(max_length=200, null=True, blank=True)
    question_requirement = models.IntegerField(default=0)
    answer_requirement = models.IntegerField(default=0)
    comment_requirement = models.IntegerField(default=0)
    vote_requirement = models.IntegerField(default=0)
    recipients = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.icon} {self.name}'



