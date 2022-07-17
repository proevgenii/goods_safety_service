from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .forms import TestOne, TestTwo, MapOne, MapTwo
from .models import OneActivity, TwoActivity
import json
import sys
from collections import defaultdict
import os
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
# Create your views here.

PATH = os.path.dirname(__file__)

coord_df = pd.read_csv(os.path.join(PATH, 'code_lat_lon.csv'))[
    ['zipcode', 'latitude', 'longitude']]

with open(os.path.join(PATH, 'dict_for_map.pkl'), 'rb') as handle:
    dct_ind = pickle.load(handle)


def get_coords(coord_df, ind_dct: dict, tn_code: str):
    """Вернет словарь с координатами для изготовителя, ИЛ и заявителя
координаты лежат в массиве в виде ["latitude", 'longitude']
ПРИМЕР:
{'izg_ind': [array([[ 37.2726, 126.9725],
             [ 40.5018, -78.41  ]])],
 'il_ind': [array([], shape=(0, 2), dtype=float64)],
 'z_ind': [array([[53.3606,  6.5981]])]})
             """
    coord_dct = defaultdict(list)
    izg_ind = ind_dct[tn_code]['i_ind']
    il_ind = ind_dct[tn_code]['il_ind']
    z_ind = ind_dct[tn_code]['z_ind']
    for ind in izg_ind:
        coord_dct['izg_ind'].append(coord_df[coord_df.zipcode == ind][[
                                    "latitude", 'longitude']].values)
    for ind in il_ind:
        coord_dct['il_ind'].append(coord_df[coord_df.zipcode == ind][[
                                   "latitude", 'longitude']].values)
    for ind in z_ind:
        coord_dct['z_ind'].append(coord_df[coord_df.zipcode == ind][[
                                  "latitude", 'longitude']].values)
    return coord_dct


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
            result = report.get_results()
            map_one = MapOne(result, form.cleaned_data)
            return render(request, 'map_1.html',
                          context={'form': map_one, 'plot_div': map_view(result["ТН ВЭД ЕАЭС"])})
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
            result = report.get_results()
            map_two = MapTwo(result)
            return render(request, 'map_2.html',
                          context={'form': map_two, 'plot_div': map_view(result["ТН ВЭД ЕАЭС"])})
        elif form.is_valid() != True:
            sys.stdout.write(json.dumps(form.errors, indent=4))
    else:
        form = TestTwo()
    context = dict()
    context['form'] = form
    return render(request, "test_2.html", context)


def map_view(tn_code):
    tittle = f'Карта безопасных товаров с ТН ВЭД ЕАЭС = {tn_code}'
    flag = True
    try:
        coord_dct = get_coords(coord_df, dct_ind, tn_code=tn_code)
        print(coord_dct)
    except Exception as e:
        tittle = "Товары не найдены"
        flag = False

    if not flag:
        x = [i for i in range(-10, 11)]
        y1 = [3*i for i in x]
        y2 = [i**2 for i in x]
        y3 = [10*abs(i) for i in x]

        graphs = []

        graphs.append(
            go.Scatter(x=x, y=y1, mode='lines', name='Line y1')
        )

        graphs.append(
            go.Scatter(x=x, y=y2, mode='markers', opacity=0.8,
                       marker_size=y2, name='Scatter y2')
        )

        graphs.append(
            go.Bar(x=x, y=y3, name='Bar y3')
        )

        layout = {
            'title': tittle,
            'xaxis_title': 'X',
            'yaxis_title': 'Y',
            'height': 420,
            'width': 560,
        }

        plot_div = plot({'data': graphs, 'layout': layout},
                        output_type='div')

    else:
        lats = []
        longs = []
        for ind in coord_dct:
            if len(coord_dct[ind][0]) > 0:
                lats.append(coord_dct[ind][0][0][0])
                longs.append(coord_dct[ind][0][0][1])
        fig = go.Figure(data=go.Scattergeo(
            lat=lats,
            lon=longs,
            # text=df['text'],
            mode='markers',
            # marker_color=df['cnt'],
        ))
        layout = {
            'title': tittle,
            'geo_scope': 'world',
            'height': 420,
            'width': 560,
        }
        plot_div = plot(go.Figure(data=fig, layout=layout).update_layout(height=300, margin={
                        "r": 0, "t": 35, "l": 0, "b": 0}), output_type='div', show_link=False)
        # plot_div = plot({'data': fig, 'layout': layout},
        #                output_type='div')

    return plot_div
