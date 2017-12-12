from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
import datetime
from .models import Question, Answer


def signin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('questions:index'))
    else:
        return render(request, 'questions/signin.html', {})


def signin_attempt(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('questions:index'))
    else:
        return HttpResponse("NOPE")


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('questions:signin'))


def register(request):
    return render(request, 'questions/register.html', {})


def activate(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.groups.add(group)
    user.save()
    login(request, user)
    return HttpResponseRedirect(reverse('wordstress:index'))


def index(request):
    questions = Question.objects.order_by('-date_time')
    return render(request, 'questions/index.html', {'questions': questions})


def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = question.answer_set.order_by('-date_time')  # related objects reference <object_name>_set.all()
    return render(request, 'questions/question_detail.html', {'question': question, 'answers': answers})


def new_question(request):
    return render(request, 'questions/new_question.html', {})


def post_question(request):
    user = request.user
    title = request.POST['title']
    body = request.POST['body']
    question = Question(user=user, title=title, body=body)
    question.save()
    return HttpResponseRedirect(reverse('questions:index'))


def post_answer(request):
    user = request.user
    answer = request.POST['answer']
    question = Question.objects.get(pk=request.POST['question_id'])
    new_answer = Answer(user=user, question=question, body=answer)
    new_answer.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')