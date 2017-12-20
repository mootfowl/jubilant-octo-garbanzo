from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body', 'tags']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']

class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=50)
