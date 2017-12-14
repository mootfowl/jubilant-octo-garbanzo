from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    # return HttpResponse(f'{request.user.profile} | user id = {user_id}')
    return render(request, 'questions/profile.html', {'user': user})


# def index(request):
#     questions = Question.objects.order_by('-date_time')
#     return render(request, 'questions/index.html', {'questions': questions})


def index(request):  # w/Paginator
    question_list = Question.objects.order_by('-date_time')
    paginator = Paginator(question_list, 7) # Show 5 questions per page

    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)

    return render(request, 'questions/index.html', {'questions': questions})


def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    question.views += 1
    question.save()
    answers = question.answer_set.order_by('-date_time')  # related objects reference <object_name>_set.all()
    question_tags = question.tags.all()
    tags = []
    for tag in question_tags:
        tags.append(tag)
    # print(tags)
    related = Question.objects.filter(tags__name__in=tags).distinct().exclude(pk=question_id)
    return render(request, 'questions/question_detail.html', {'question': question, 'answers': answers, 'tags': tags, 'related': related})


def new_question(request):
    return render(request, 'questions/new_question.html', {})


def post_question(request):
    user = request.user
    user.profile.questions += 1
    user.profile.save()
    title = request.POST['title']
    body = request.POST['body']
    tags = request.POST['tags'].split(', ')
    # print(tags)
    question = Question(user=user, title=title, body=body)
    question.save()  # It appears to be necessary to save the instance before .tags.add() is executed
    for tag in tags:
        question.tags.add(tag)
    question.save()
    return HttpResponseRedirect(reverse('questions:index'))


def post_answer(request):
    user = request.user
    user.profile.answers += 1
    user.profile.save()
    answer = request.POST['answer']
    question = Question.objects.get(pk=request.POST['question_id'])
    new_answer = Answer(user=user, question=question, body=answer)
    new_answer.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')


def search(request):
    terms = request.POST['search'].split()
    questions = Question.objects.filter(tags__name__in=terms, body__name__in=terms).distinct()
    # print(questions)
    return render(request, 'questions/search.html', {'terms': terms, 'questions': questions})


def solve(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    question = answer.question
    user = answer.user
    user.profile.solutions += 1
    user.profile.save()
    question.solved = True
    question.save()
    answer.solution = True
    answer.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')
