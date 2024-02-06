import os
import re

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

files = [file for file in os.listdir() if re.match(r'\d{4}_\d{2}V\d{2}.*\.csv', file)]

files_result = [file for file in os.listdir() if re.match(r'\d{4}_\d{2}V\d{2}\.result.log', file)]


with open(f'{files_result[0]}') as f1:
    for line in f1:
        if 'P50' in line:
            p50_1 = round(float(line.split('=')[1]),3)
        if 'P95' in line:
            p95_1 = round(float(line.split('=')[1]),3)
        if 'HRMS' in line:
            HRMS_1 = round(float(line.split('=')[1]),3)
            break
with open(f'{files_result[0]}') as f2:
    for line in f2:
        if 'P50' in line:
            p50_2 = round(float(line.split('=')[1]),3)
        if 'P95' in line:
            p95_2 = round(float(line.split('=')[1]),3)
        if 'HRMS' in line:
            HRMS_2 = round(float(line.split('=')[1]),3)
            break
with open(f'{files_result[0]}') as f3:
    for line in f3:
        if 'P50' in line:
            p50_3 = round(float(line.split('=')[1]),3)
        if 'P95' in line:
            p95_3 = round(float(line.split('=')[1]),3)
        if 'HRMS' in line:
            HRMS_3 = round(float(line.split('=')[1]),3)
            break


with open(f'{files[0]}') as f1:
    name1 = f1.name.split(".")[0]
    hor_err1 = f1.read().split(',')
    hor_err1 = [float(x) for x in hor_err1]
    fig1 = px.ecdf(hor_err1)
    fig1.update_traces(line_color='red')
    fig1['data'][0]['showlegend'] = True
    fig1['data'][0]['hovertemplate'] = '<br>Value=%{x}<br>Probability=%{y}<extra></extra>'
    fig1['data'][0]['legendgroup'] = 0
    fig1['data'][0]['legendgrouptitle']['text'] = f'HRMS = {HRMS_1}<br>P50 = {p50_1}<br>P95 = {p95_1}'
    fig1['data'][0]['name'] = name1



with open(f'{files[1]}') as f2:
    name2 = f2.name.split(".")[0]
    hor_err2 = f2.read().split(',')
    hor_err2 = [float(x) for x in hor_err2]
    fig2 = px.ecdf(hor_err2)
    fig2.update_traces(line_color='green')
    fig2['data'][0]['showlegend'] = True
    fig2['data'][0]['hovertemplate'] = '<br>Value=%{x}<br>Probability=%{y}<extra></extra>'
    fig2['data'][0]['legendgroup'] = 1
    fig2['data'][0]['legendgrouptitle']['text'] = f'HRMS = {HRMS_2}<br>P50 = {p50_2}<br>P95 = {p95_2}'
    fig2['data'][0]['name'] = name2

with open(f'{files[2]}') as f3:
    name3 = f3.name.split(".")[0]
    hor_err3 = f3.read().split(',')
    hor_err3 = [float(x) for x in hor_err3]
    fig3 = px.ecdf(hor_err3)
    fig3.update_traces(line_color='blue')
    fig3['data'][0]['showlegend'] = True
    fig3['data'][0]['hovertemplate'] = '<br>Value=%{x}<br>Probability=%{y}<extra></extra>'
    fig3['data'][0]['legendgroup'] = 2
    fig3['data'][0]['legendgrouptitle']['text'] = f'HRMS = {HRMS_3}<br>P50 = {p50_3}<br>P95 = {p95_3}'
    fig3['data'][0]['name'] = name3




fig = go.Figure(data = fig1.data + fig2.data + fig3.data, layout=fig1.layout)
fig.update_layout(title_text="Empirical Cumulative Distribution Function", title_x=0.5)
fig.update_layout(legend_title=None)
# fig.update_layout(legend_groupclick="toggleitem")
# fig.update_layout(legend_bordercolor='#00a86b')
# fig.update_layout(legend_borderwidth=1)
fig.update_layout(legend_tracegroupgap=60)


fig.write_html("cdf.html")