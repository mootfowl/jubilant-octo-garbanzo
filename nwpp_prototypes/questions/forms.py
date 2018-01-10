from django import forms
from django.forms import ModelForm
from ckeditor.widgets import CKEditorWidget
from .models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'category', 'body', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}),
            # 'category': forms.Select(attrs={'placeholder': 'Category'}), # <-- This doesn't work...
            'tags': forms.TextInput(attrs={'placeholder': 'Tags, separated by commas', 'class': 'form-control'}),
            'body': forms.CharField(widget=CKEditorWidget)
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['body']



