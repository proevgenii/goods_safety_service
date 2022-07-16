from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import TestOne, TestTwo
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
            report.code = form.cleaned_data["code"]
            report.common_naming = form.cleaned_data["common_naming"]

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
            return render(request, 'map.html',
                          context={'plot_div': plot_div})
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = TestTwo()
    context = dict()
    context['form'] = form
    return render(request, "test_2.html", context)


@ensure_csrf_cookie
def map_view(request):
    px.set_mapbox_access_token(open(".mapbox_token").read())
    df = px.data.carshare()
    graphs = []
    graphs.append(px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10))
    layout = {
        'title': 'Title of the figure',
        'xaxis_title': 'X',
        'yaxis_title': 'Y',
        'height': 420,
        'width': 560,
    }

    plot_div = plot({'data': graphs, 'layout': layout},
                    output_type='div')

    return render(request, 'map.html',
                  context={'plot_div': plot_div})
