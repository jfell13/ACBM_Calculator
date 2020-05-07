import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#import matplotlib.plot as plt
import numpy as np
import plotly.graph_objs as go
import os
#import pandas as pd
import base64
import webbrowser
from threading import Timer

#### Initial Data and Constants >>>> Hours = X, Cost = Y #########
start_Hours = np.array(range(0,105,5)) # Starting Values (X)
Hours = start_Hours

# Achievable cell concentration cells/mL
ACC = ["{:e}".format(10000000),"{:e}".format(95000000),"{:e}".format(95000000),"{:e}".format(200000000)] 
# FGF-2 conc. (g/L)
FGF2Con = ["{:e}".format(0.0001),"{:e}".format(0.00005),"{:e}".format(0.00005),"{:e}".format(0.0)]
# FGF-2 cost (USD/g)
FGF2Cost = ["{:e}".format(4010000),"{:e}".format(2010000),"{:e}".format(0),"{:e}".format(0)]
# Glucose concentration in basal media (mol/L)
GCinBM = ["{:e}".format(0.0178),"{:e}".format(0.0267),"{:e}".format(0.0267),"{:e}".format(0.0356)]
# Glu. cons. rate per cell (mol/ h cell)
Ug = ["{:e}".format(0.000000000000413),"{:e}".format(0.000000000000207),"{:e}".format(0.000000000000207),"{:e}".format(0.0000000000000413),] 
d = [24.0, 16.0, 16.0, 8.0] # Hours per doubling (h)
MatTime = [240, 156, 156, 24] # Maturation Time (h)

# Fixed Constants
BRWV = float(20.0*1000000) # Bioreactor working volume (m3^)
BioRScF = float(0.60) # Bioreactor Scale Factor
Adj_BioR_valu = float(1.29)
BioReCost = float(50000)
Des_MMeat_Pro = float(119000000)
FGF2MM = float(24000)
tot_fixed_eq_costs = 2 * Adj_BioR_valu * BioReCost * (BRWV**BioRScF)

BIOREACTORS = [5205,360,360,49] # Bioreactor numbers
cust_Bio_react = 1

Cost1 = Hours * BIOREACTORS[0] * tot_fixed_eq_costs #* float(ACC[0]) * float(BRWV) * float(Ug[0]) *FGF2MM * float(FGF2Cost[0])
Cost2 = Hours * BIOREACTORS[1] * tot_fixed_eq_costs #* float(ACC[1]) * float(BRWV) * float(Ug[1]) *FGF2MM * float(FGF2Cost[1])
Cost3 = Hours * BIOREACTORS[2] * tot_fixed_eq_costs #* float(ACC[2]) * float(BRWV) * float(Ug[2]) *FGF2MM * float(FGF2Cost[2])
Cost4 = Hours * BIOREACTORS[3] * tot_fixed_eq_costs #* float(ACC[3]) * float(BRWV) * float(Ug[3]) *FGF2MM * float(FGF2Cost[3])
Cust_Cost = Hours * cust_Bio_react * tot_fixed_eq_costs
#### Scenario Cost Traces #######

Cost1_trace = go.Scatter(x=Hours,y=Cost1,
                         mode="lines+markers",
                         name="Scenario 1",
                         marker = dict(color = 'firebrick'),
                         line = dict(color='firebrick', width=2),
                         hovertemplate='Scenario 1<br>Time: %{x}<br>Cost: %{y}<extra></extra>')
Cost2_trace = go.Scatter(x=Hours,y=Cost2,
                         mode="lines+markers",
                         name="Scenario 2",
                         marker = dict(color = '#FFA505'),
                         line = dict(color='#FFA505', width=2),
                         hovertemplate='Scenario 2<br>Time: %{x}<br>Cost: %{y}<extra></extra>')
Cost3_trace = go.Scatter(x=Hours,y=Cost3,
                         mode="lines+markers",
                         name="Scenario 3",
                         marker = dict(color='royalblue'),
                         line = dict(color='royalblue', width=2),
                         hovertemplate='Scenario 3<br>Time: %{x}<br>Cost: %{y}<extra></extra>')
Cost4_trace = go.Scatter(x=Hours,y=Cost4,
                         mode="lines+markers",
                         name="Scenario 4",
                         marker = dict(color='teal'),
                         line = dict(color='teal', width=2),
                         hovertemplate='Scenario 4<br>Time: %{x}<br>Cost: %{y}<extra></extra>')

#### Custom Cost Trace ####

Custom_trace = go.Scatter(x=Hours,y=Cust_Cost,
                         mode="lines+markers",
                         name="Custom Cost",
                         marker = dict(color='#781c6d'),
                         line = dict(color='#781c6d', width=2),
                         hovertemplate='Custom Cost<br>Time: %{x}<br>Cost: %{y}<extra></extra>')

#### Figure Things

Cost_data = [Cost1_trace,Cost2_trace,Cost3_trace,Cost4_trace,Custom_trace]
fig_layout = go.Layout(
    title="Cost per Hour", 
    xaxis={'title':'Time (Hr)','range':[min(Hours),max(Hours)]}, 
    yaxis={'title':'Cost ($/Hr)'},
    margin=go.layout.Margin(t=100))
Fig = go.Figure(dict(data = Cost_data, layout = fig_layout))

#### Dash Things

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'The_University_of_California_Davis.svg.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    
    # Block 1: Logo and Words
    html.Div([ 
        html.Div([ # Left side: Logo
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'25%', 'width':'25%'})
            ], className="six columns"),
        html.Div([ # Right Side: Some words
            html.H1(children='Big Words #1',
                   style={
                    'textAlign': 'center'})#,
#             html.H1(children='Big Words #2',
#                    style={
#                     'textAlign': 'center'})
            ], className="six columns"),
    ], className="row"),
    
    # Second block: Author(s) and info
    html.Div(children='''
            This Cell-Based-Meat calculator app was written by Dr. Jason S. Fell.
    '''),
    
    # Thirds block: Graph and sliders
    html.Div([
        html.Div([
            dcc.Graph(
                id='graph',
                figure=Fig,
                style={'padding':10}#'height': 300, 'width': 700},
                ),
            dcc.RangeSlider(
                id='graph-slider',
                min=start_Hours.min(), # Scale values based on starting hours
                max=start_Hours.max(),
                value=[start_Hours.min(),start_Hours.max()],
                marks={str(i): str(i) for i in start_Hours},
                step=1.0,
                allowCross=False
                ), 
        ], className="six columns",style={'marginBottom': 20}),
        html.Div([
#             html.Label('Bioreactors',
#                 style={'textAlign': 'center'}),
            html.Div([
                html.I("Adjust the number of bioreactors.")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'bioreactslider',
                    min = 1,
                    max = 2*max(BIOREACTORS),
                    value = int(cust_Bio_react),
                    #marks = {str(i): str(i) for i in range(min(BIOREACTORS),max(BIOREACTORS))},
                    step=1.0
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                dcc.Input(id="bioreact", 
                          type='number', 
                          #min=1,
                          #max=2*max(BIOREACTORS),
                          value = int(cust_Bio_react),
                          step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
            html.Div([
                html.Div(id="output",
                        children=u'The number of bioreactors is set to {}'.format(cust_Bio_react)
                        )],
                style={'marginBottom': 10,'marginTop': 10})
        ], className="six columns")
        ], className="row"),
    
    # Fourth block: other
    html.Div([    
        dcc.LogoutButton(id="logout")],
        style={'marginBottom': 10,'marginTop': 10})
])


@app.callback(
    Output('graph', 'figure'),
    [Input('graph-slider', 'value'),
    Input('bioreactslider','value')])

def update_figure(selected,slider1_input):
    '''Function to update plot scale of graph1 from 
    the range slider . Input is list 
    with 2 data points lower and upper scale ends.'''
    
    cust_Bio_react = slider1_input
    new_Cust_Cost = Hours * cust_Bio_react * tot_fixed_eq_costs
    new_Custom_trace = go.Scatter(x=Hours,y=new_Cust_Cost,
                         mode="lines+markers",
                         name="Custom Cost",
                         marker = dict(color='#781c6d'),
                         line = dict(color='#781c6d', width=2),
                         hovertemplate='Custom Cost<br>Time: %{x}<br>Cost: %{y}<extra></extra>')
    new_Cost_data = [Cost1_trace,Cost2_trace,Cost3_trace,Cost4_trace,new_Custom_trace]
    
    new_fig_layout = go.Layout(
        title="Cost per Hour", 
        xaxis={'title':'Time (Hr)','range':[min(selected),max(selected)]}, 
        yaxis={'title':'Cost ($/Hr)'},
        margin=go.layout.Margin(t=100))
    
    return {
    'data': new_Cost_data, # Cost data
    'layout': new_fig_layout # New figure layout with altered X-axis scale
    }

#### Testing Chained Callbacks #######

@app.callback(
    Output('output', 'children'),
    [Input('bioreactslider','value')])

def update_scale1_output1(bioreactslider_input):
    if bioreactslider_input > 2*max(BIOREACTORS):
        bio_output = 2*max(BIOREACTORS)
    else:
        bio_output = bioreactslider_input
    return u'The number of bioreactors is set to {}'.format(bio_output)

@app.callback(
    Output('bioreactslider','value'),
    [Input('bioreact', 'value')])
    
def update_scale(bioreact_input):
    if bioreact_input == None:
        bioreact = 1
    else:
        if bioreact_input > 2*max(BIOREACTORS):
            bioreact = 2*max(BIOREACTORS)
        else:
            bioreact = bioreact_input
    return bioreact

#### App launching functions ######

port = 8050 

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))
    
application = app.server

if __name__ == '__main__':
    Timer(0, open_browser).start();
    app.run_server(debug=True, port=port)
