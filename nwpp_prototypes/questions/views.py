from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import datetime
import json
from .models import Question, Answer, Badge, Profile, Notification, Category, Vote
from .forms import QuestionForm, AnswerForm


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
    return HttpResponseRedirect(reverse('questions:index'))


def register(request):
    return render(request, 'questions/register.html', {})


def activate(request):
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    group = Group.objects.get(name='Contributors')
    user.groups.add(group)
    user.save()
    user_profile = Profile(user=user)
    user_profile.save()
    login(request, user)
    return HttpResponseRedirect(reverse('questions:index'))


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    # return HttpResponse(f'{request.user.profile} | user id = {user_id}')
    return render(request, 'questions/profile.html', {'user': user})


def edit_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = user.profile


def index(request):  # w/Paginator
    question_list = Question.objects.order_by('-created')
    paginator = Paginator(question_list, 20) # Show 20 questions per page
    page = request.GET.get('page')
    try:
        questions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        questions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        questions = paginator.page(paginator.num_pages)
    # < FOR TESTING PURPOSES >
    # print(request.user.vote_set.all())
    # < END TEST >
    return render(request, 'questions/index.html', {'questions': questions})


def question_detail(request, question_id):
    if request.user.is_authenticated:
        user = request.user
        user.profile.views += 1
        user.profile.save()
    question = Question.objects.get(pk=question_id)
    question.views += 1
    question.save()
    answers = question.answer_set.order_by('-created')  # related objects reference <object_name>_set.all()
    # < TEST >
    # < END TEST >
    question_tags = question.tags.all()
    tags = []
    for tag in question_tags:
        tags.append(tag)
    related = Question.objects.filter(tags__name__in=tags).distinct().exclude(pk=question_id)
    form = AnswerForm()
    return render(request, 'questions/question_detail.html', {'question': question, 'answers': answers, 'tags': tags, 'related': related, 'form': form})


def new_question(request):
    form = QuestionForm()
    return render(request, 'questions/new_question.html', {'form': form})


def edit_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    form = QuestionForm(instance=question)
    if form.is_valid():
        form.save()
    return render(request, 'questions/new_question.html', {'question': question, 'form': form, 'edit': True})


def save_question(request, question_id):
    user = request.user
    user.profile.edits += 1
    user.profile.save()
    question = Question.objects.get(pk=question_id)
    title = request.POST['title']
    category = request.POST['category']
    body = request.POST['body']
    tags = request.POST['tags'].split(', ')
    question.title = title
    question.category = Category.objects.get(pk=category)
    question.body = body
    question.tags = tags
    question.save()
    return question_detail(request, question_id)


def post_question(request):
    user = request.user
    user.profile.questions += 1
    user.profile.save()
    title = request.POST['title']
    category = Category.objects.get(pk=request.POST['category'])
    body = request.POST['body']
    tags = request.POST['tags'].split(', ')
    # print(tags)
    question = Question(user=user, title=title, category=category, body=body)
    question.save()  # It appears to be necessary to save the instance before .tags.add() is executed
    for tag in tags:
        question.tags.add(tag)
    question.save()
    return index(request)


def post_answer(request):
    user = request.user
    user.profile.answers += 1
    user.profile.save()
    answer = request.POST['body']
    question = Question.objects.get(pk=request.POST['question_id'])
    new_answer = Answer(user=user, question=question, body=answer)
    new_answer.save()
    notification = Notification(from_user=user, to_user=question.user, question=question, answer=new_answer, notification_type='a')
    notification.save()
    # print(request.user.notification_set.all())
    return HttpResponseRedirect(f'../question_detail/{question.id}')


def comment(request):
    pass


def search(request):
    if request.user.is_authenticated:
        user = request.user
        user.profile.searches += 1
        user.profile.save()
    terms = request.POST['search'].split()
    questions = Question.objects.filter(tags__name__in=terms).distinct()
    return render(request, 'questions/search.html', {'terms': terms, 'questions': questions})


# def search(request):
#     terms = request.POST['search'].split()
#     questions = Question.objects.filter(tags__name__in=terms, body__search=terms).distinct()
#     return render(request, 'questions/search.html', {'terms': terms, 'questions': questions})


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
    notification = Notification(from_user=request.user, to_user=answer.user, question=question, answer=answer, notification_type='s')
    notification.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')


def tags(request):
    all_tags = Tag.objects.all().distinct()
    categories = Category.objects.all()
    return render(request, 'questions/tags.html', {'all_tags': all_tags, 'categories': categories})


def voteup(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    answer.vote_counter += 1
    answer.save()
    question = answer.question
    user = request.user
    user.profile.vote_counter += 1
    user.profile.save()
    vote = Vote(user=user, answer=answer, vote_type='u')
    vote.save()
    notification = Notification(from_user=request.user, to_user=answer.user, question=question, answer=answer, notification_type='v')
    notification.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')


def votedown(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    answer.vote_counter -= 1
    answer.save()
    question = answer.question
    user = request.user
    user.profile.vote_counter += 1  # votes up or down still increase total user.profile vote_counter
    user.profile.save()
    vote = Vote(user=user, answer=answer, vote_type='d')
    vote.save()
    return HttpResponseRedirect(f'../question_detail/{question.id}')


def clear_all(request):
    request.user.notification_set.all().delete()
    return index(request)


def flag_check(request):
    pass
#   when a flag is confirmed, flag_check will be run to tally the total number of flags and determine outcome


def flag(request):
    pass


# def badge_check(user):  ## move to user.profile method?
#     badges = Badge.objects.all()
#     for badge in badges:
#         if user.profile.questions >= badge.question_requirement:
#             return badge
#         else:
#             return