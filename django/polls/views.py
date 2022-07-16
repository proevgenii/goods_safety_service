from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import TestOne, TestTwo
from .models import OneActivity, TwoActivity
import json
import sys
# Create your views here.

@ensure_csrf_cookie
def test_1_view(request):
    if request.method == "POST":
        form = TestOne(request.POST or None)
        if form.is_valid():
            report = OneActivity()
            report.code= form.cleaned_data["code"]
            report.common_naming = form.cleaned_data["common_naming"]
            report.tn_ved = form.cleaned_data["tn_ved"]
            report.tech_req = form.cleaned_data["tech_req"]
            report.group_prod = form.cleaned_data["group_prod"]
            return render(request, "map.html")
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = TestOne()
    context = dict()
    context['form'] = form
    return render(request, "test_1.html", context)

@ensure_csrf_cookie
def result_view(request):
    return render(request, "map.html")

@ensure_csrf_cookie
def test_2_view(request):
    if request.method == "POST":
        form = TestTwo(request.POST or None)
        if form.is_valid():
            report = TwoActivity()
            report.code= form.cleaned_data["code"]
            report.common_naming = form.cleaned_data["common_naming"]
            return render(request, "map.html")
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = TestTwo()
    context = dict()
    context['form'] = form
    return render(request, "test_2.html", context)
