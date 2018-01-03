import random
# from django.contrib.auth.models import User, Group, Permission
# from .models import Question, Answer, Profile, Notification, Category


questions = ['How many licks does it take to get to the tootsie roll center of a tootsie pop?',
             'Are you my mother?',
             'Can you tell me how to get to Sesame Street?',
             "Why are there so many songs about rainbows and what's on the other side?",
             'What are the chances?',
             "Why can't I feel my legs?",
             "Where did all the time go?",
             "Is this thing on?",
             "What is the meaning of life?",
             "Is there life after death?",
             "Where's Waldo?"
             ]


def generate_question():
    custom_question = ''
    for i in range(len(questions)):
        custom_question += questions[random.randint(0, len(questions) - 1)]
        custom_question += '\n'
    return custom_question


print(generate_question())

