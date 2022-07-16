from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import TestOne, TestTwo, MapOne
from .models import OneActivity, TwoActivity
import json
import sys
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
# Create your views here.


@ensure_csrf_cookie
def test_1_view(request):
    if request.method == "POST":
        form = TestOne(request.POST or None)
        if form.is_valid():
            report = OneActivity()
            report.code = form.cleaned_data["code"]
            report.common_naming = form.cleaned_data["common_naming"]
            report.tn_ved = form.cleaned_data["tn_ved"]
            report.tech_req = form.cleaned_data["tech_req"]
            report.group_prod = form.cleaned_data["group_prod"]
            map_one=MapOne(OneActivity.get_results())
            return render(request, 'map_1.html',
                          context={'form': map_one,'plot_div': map_view()})
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
            report.code = form.cleaned_data["code"]
            report.common_naming = form.cleaned_data["common_naming"]
            print(TwoActivity.get_results())
            return render(request, 'map.html',
                          context={'plot_div': map_view()})
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = TestTwo()
    context = dict()
    context['form'] = form
    return render(request, "test_2.html", context)


def map_view():
    x = [i for i in range(-10, 11)]
    y1 = [3*i for i in x]
    y2 = [i**2 for i in x]
    y3 = [10*abs(i) for i in x]

    # List of graph objects for figure.
    # Each object will contain on series of data.
    graphs = []

    # Adding linear plot of y1 vs. x.
    graphs.append(
        go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
    )

    # Adding scatter plot of y2 vs. x.
    # Size of markers defined by y2 value.
    graphs.append(
        go.Scatter(x=x, y=y2, mode='markers', opacity=0.8,
                   marker_size=y2, name='Scatter y2')
    )

    # Adding bar plot of y3 vs x.
    graphs.append(
        go.Bar(x=x, y=y3, name='Bar y3')
    )

    # Setting layout of the figure.
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')

    return plot_div
