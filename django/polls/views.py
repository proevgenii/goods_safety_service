from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import UserForm, ProjectForm
from .models import UserActivity, ProjectActivity
import json
import sys
# Create your views here.

@ensure_csrf_cookie
def test_1_view(request):
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            report = UserActivity()
            report.team_member = form.cleaned_data["team_member"]
            report.team = form.cleaned_data["team"]
            report.status = form.cleaned_data["status"]
            report.team_member_backup = form.cleaned_data["team_member_backup"]
            report.assigned_projects = form.cleaned_data["assigned_projects"]
            report.achievements = form.cleaned_data["achievements"]
            report.project_end_date = form.cleaned_data["project_end_date"]
            report.invoke_lambda(report.build_report())
            return render(request, "map.html")
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = UserForm()
    context = dict()
    context['form'] = form
    return render(request, "test_1.html", context)

@ensure_csrf_cookie
def result_view(request):
    return render(request, "map.html")

@ensure_csrf_cookie
def test_2_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST or None)
        if form.is_valid():
            invoker = UserActivity()
            report = ProjectActivity()
            report.team_member = form.cleaned_data["team_member"]
            report.project = form.cleaned_data["project"]
            report.project_name = form.cleaned_data["project_name"]
            report.last_week_achievements = form.cleaned_data["last_week_achievements"]
            report.last_project_updates = form.cleaned_data["last_project_updates"]
            report.next_week_achievements = form.cleaned_data["next_week_achievements"]
            report.next_project_updates = form.cleaned_data["next_project_updates"]
            invoker.invoke_lambda(report.build_report())
            return render(request, "map.html")
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = ProjectForm()
    context = dict()
    context['form'] = form
    return render(request, "test_2.html", context)
