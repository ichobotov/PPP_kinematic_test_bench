import os
import re

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

files = [file for file in os.listdir() if re.match(r'\d{4}_\d{2}V\d{2}\.csv', file)]


with open(f'{files[0]}') as f1:
    name1 = f1.name.split(".")[0]
    hor_err1 = f1.read().split(',')
    hor_err1 = [float(x) for x in hor_err1]
    fig1 = px.ecdf(hor_err1, title="Empirical Cumulative Distribution Function")
    fig1.update_traces(line_color='red')
    fig1['data'][0]['showlegend'] = True
    fig1['data'][0]['name'] = name1
with open(f'{files[1]}') as f2:
    name2 = f2.name.split(".")[0]
    hor_err2 = f2.read().split(',')
    hor_err2 = [float(x) for x in hor_err2]
    fig2 = px.ecdf(hor_err2, title="Empirical Cumulative Distribution Function")
    fig2.update_traces(line_color='green')
    fig2['data'][0]['showlegend'] = True
    fig2['data'][0]['name'] = name2
with open(f'{files[2]}') as f3:
    name3 = f3.name.split(".")[0]
    hor_err3 = f3.read().split(',')
    hor_err3 = [float(x) for x in hor_err3]
    fig3 = px.ecdf(hor_err3, title="Empirical Cumulative Distribution Function")
    fig3.update_traces(line_color='blue')
    fig3['data'][0]['showlegend'] = True
    fig3['data'][0]['name'] = name3


fig = go.Figure(data = fig1.data + fig2.data + fig3.data)
fig.write_html("cdf.html")