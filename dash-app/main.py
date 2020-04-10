import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import matplotlib
#import plotly.graph_objs as go
#import plotly.offline as py
import os
import pandas as pd
#from PIL import Image, ImageTk
import base64

data = [[0,1,2,3,4,5],[2,4,6,8,10,12],[3,4,7,8,9,11]]
df = pd.DataFrame(data,columns=[1,2,3,4,5,6], index =['Series 1','Series 2','Series 3'])
df_f = df.transpose()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = './The_University_of_California_Davis.svg.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'10%', 'width':'10%'}),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='slider',
        min=df_f.index.min(),
        max=df_f.index.max(),
        value=df_f.index.max(),
        marks={str(i): str(i) for i in df_f.index.unique()},
        step=None
    )#,
    #html.Label('Dropdown'),
    #dcc.Dropdown(
        #id='series',
        #options=[
            #{'label': 'All Series', 'value': 'all'},
            #{'label': 'Series 1', 'value': 'Series 1'},
            #{'label': 'Series 2', 'value': 'Series 2'},
            #{'label': 'Series 2', 'value': 'Series 3'}
        #],
        #value='all'
    #),
    
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('slider', 'value')])#,
    #Input('series', 'value')])

def update_figure(selected_num):
    filtered_df = df_f.loc[0:selected_num]
    traces = []
    #if sel_series == "all":    
    for i in filtered_df:
        df_by_filter = filtered_df[i]
        traces.append(dict(
                        x=df_by_filter.index,
                        y=df_by_filter,
                        text=df_by_filter,
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 10,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                ))
    #else:
        #for i in filtered_df:
            #if i == sel_series:
                #df_by_filter = filtered_df[i]
                #traces.append(dict(
                            #x=df_by_filter.index,
                            #y=df_by_filter,
                            #text=df_by_filter,
                            #mode='markers',
                            #opacity=0.7,
                            #marker={
                                #'size': 10,
                                #'line': {'width': 0.5, 'color': 'white'}
                            #},
                            #name=i
                    #))
            #else:
                #pass
    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'linear', 'title': 'X Values (Bacon)',
                   'range':[0, selected_num]},
            yaxis={'title': 'Bacon Consumption (Kg/Yr)', 'range': [0, 15]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)