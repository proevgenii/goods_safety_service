from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World, вы в polls")


def detail(request, question_id):
    return HttpResponse("Вы просматриваете вопрос %s." % question_id)


def results(request, question_id):
    response = "Перед вами результаты вопроса %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("Вы голосуете за вопрос %s." % question_id)
