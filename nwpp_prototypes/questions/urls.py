"""dp_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'questions'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signin_attempt/$', views.signin_attempt, name='signin_attempt'),
    url(r'^signout/$', views.signout, name='signout'),
    url(r'^question_detail/(?P<question_id>[0-9]+)$', views.question_detail, name='question_detail'),
    url(r'^new_question/$', views.new_question, name='new_question'),
    url(r'^post_question/$', views.post_question, name='post_question'),
    url(r'^post_answer/$', views.post_answer, name='post_answer'),
    url(r'^register/$', views.register, name='register'),
    url(r'^activate/$', views.activate, name='activate'),
    url(r'^profile/(?P<user_id>[0-9+])$', views.profile, name='profile'),
    url(r'^search/$', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
