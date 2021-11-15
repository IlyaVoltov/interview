# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_table
from dash_table.Format import Sign
import pandas as pd
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('data//data.csv', 
    usecols=['Index', 'Question', 'Tag', 'Comment', 'Score', 'Summ', 'Name'])

column_names = [{"name": "Номер вопроса", "id": "Index"},
                {"name": "Вопрос", "id": "Question"},
                {"name": "Тема", "id": "Tag"},
                {"name": "Комментарий", "id": "Comment"},
                {"name": "Оценка", "id": "Score"}
                ]

x = [
    ["Соискатель - Планка", "Соискатель - Всего"],
    [1, 2]
]

fig = go.Figure()
fig.add_bar(x=x,y=[20.3, 20.3], name='Соискатель')
fig.add_bar(x=x,y=[4.45, 12.7], name='Целевой показатель')
fig.update_layout(barmode="relative")

colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen', 'blue', 'red', 'grey' ]

figar = go.Figure(data=[go.Pie(labels=['общие вопросы (5 вопросов)', 'основы JS (4 вопроса)', 'GIT (6 вопросов)', 'основы сетей и протоколов (6 вопросов)', 'testing pyramid (3 вопроса)', 'Java Script (8 вопросов)', 'дополнительный вопрос (1 вопрос)'], 
                             values=[3.6,3.6,3.1,2.2,0.3,6.5,1])])
figar.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))

PAGE_SIZE=8

def generate_table():
    measure_table = dash_table.DataTable(
        id='datatable-paging',
        columns=column_names,
        data=df.to_dict('records'),

        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',
        #sort_action='native',
        editable=True,

        style_data={
            'textAlign': 'left',
            'whiteSpace': 'normal',
	        'height': 'auto',
        },
        style_cell={
            'textAlign': 'left',
	        'fontsize': '17px',
        },
                style_data_conditional=[
        {
            'if': {
                 'filter_query': '{Score} = 0,3', # comparing columns to each other
                'column_id': 'Score'
            },
            'backgroundColor': 'rgb(176, 9, 9)',
            'color': 'white',
            'font-weight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Score} = 0', # comparing columns to each other
                'column_id': 'Score'
            },
            'backgroundColor': 'red',
            'color': 'white',
            'font-weight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Score} > 0,3', # comparing columns to each other
                'column_id': 'Score'
            },
            'backgroundColor': 'rgb(90,255,170)',
            'color': 'black',
            'font-weight': 'bold'
        },
        {
            'if': {
                'filter_query': '{Tag} = "Ответ неверный."', # comparing columns to each other
                'column_id': 'Tag'
            },
            'backgroundColor': 'red',
            'color': 'white',
            'font-weight': 'bold'
        }
        ],
    )

    return measure_table

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Собеседование на позицию Front-end developer. Повышение заработной платы.', style={
        'textAlign': 'center',
        'position': 'relative', 
        'background': '#8f53ee', 
        'color': '#fff',
        'padding': '1em 2em'
    }),
    html.Div(children='''
        09 - 10.09.2021 Степалин Иван Игоревич
    ''',style={
        'font-weight': 'bold',
        'position': 'relative', 
        'padding': '13px',
        'margin': '8px'}),
    html.Div(children='''
        Темы: общие вопросы; основы JS; GIT; основы сетей и протоколов;testing pyramid; Java Script;
    ''', style={
        'font-weight': 'bold',
        'padding': '13px',
        'margin': '8px'}),
    html.Div(children='''
        Балл соискателя: 20,3 Всего баллов: 33
    ''', style={
        'font-weight': 'bold',
        'padding': '13px',
        'margin': '8px'}),
     generate_table(),
    
dcc.Graph(figure=fig,
        id='example-graph',
        style={
        'font-weight': 'bold',
        'padding': '20px',
        'margin': '15px'}
    ),

dcc.Graph(figure=figar,
        id='e-graph'
    )
])


@app.callback(
    Output('datatable-paging', 'data'),
    [
        Input('datatable-paging', "page_current"),
        Input('datatable-paging', "page_size")
    ]
)
def update_table(page_current, page_size):
    dff = df
    return dff.iloc[
        page_current * page_size:(page_current + 1 ) * page_size
    ].to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=True)

    