import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objs as go
#import plotly.express as px
import os
import base64
import webbrowser
from threading import Timer
from fixed_constants import *
from bioreactor_and_media import *

#### Data Lists #####

Scenarios = ["Scenario 1","Scenario 2","Scenario 3","Scenario 4","Custom Scenario"]
Costs_Bioequip = [BioEquip1,BioEquip2,BioEquip3,BioEquip4,BioEquip_Cust]
Costs_BioEquipTotal = [BioEquip1_total,BioEquip2_total,BioEquip3_total,BioEquip4_total,BioEquip_Cust_total]
Costs_Fixed_Manu = [Fix_Manu_Cost1,Fix_Manu_Cost2,Fix_Manu_Cost3,Fix_Manu_Cost4,Fix_Manu_Cust_Cost]
Media_Vol = []
Media_Costs = [AnnMediaCost1,AnnMediaCost2,AnnMediaCost3,AnnMediaCost4,cust_AnnMediaCost]
Ann_Media_Cost = []

#### Scenario Cost Traces #######

fig = go.Figure()

fig.add_trace(go.Bar(
    x=Scenarios,
    y=Costs_Bioequip,
    name='Bioreactor Costs',
    marker_color='indianred',
    offsetgroup=0,
    hovertemplate='Scenario: %{x}<br>Bioreactor Cost: %{y}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=Scenarios,
    y=Costs_BioEquipTotal,
    name='Fixed Total Bioreactor Costs',
    marker_color='#FFA505',
    mode="markers",
    #offsetgroup=0,
    #base=Costs_Bioequip,
    hovertemplate='Scenario: %{x}<br>Fixed Total Bioreactor Cost: %{y}<extra></extra>'
))

fig.add_trace(go.Bar(
    x=Scenarios,
    y=Costs_Fixed_Manu,
    name='Fixed Manufacturing Cost',
    marker_color='firebrick',
    offsetgroup=1,
    hovertemplate='Scenario: %{x}<br>Fixed Manufacturing Cost: %{y}<extra></extra>'
))

fig.add_trace(go.Bar(
    x=Scenarios,
    y=Media_Costs,
    name='Annual Media Cost',
    marker_color='teal',
    offsetgroup=2,
    hovertemplate='Scenario: %{x}<br>Annual Media Cost: %{y}<extra></extra>'
))

fig.update_layout(xaxis_tickangle=45, yaxis_type="log", yaxis_title="US Dollars ($)")

#### Dash Things

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_filename = 'The_University_of_California_Davis.svg.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([     
    html.Div([ # Block 1: Logo, Graph, and Custom Variables with Outputs
        html.Div([ # Left side: Logo
            html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'height':'25%', 'width':'25%'}),
            html.Div(children='This Cell-Based-Meat calculator app was written by Dr. Jason S. Fell.'),
            html.Div(children='The desired mass of meat being produced is 121,000,000 kg.'),
            html.Div([
                dcc.Graph( # Output of Graphs and Custom Values
                    id='graph',
                    figure=fig,
                    style={'padding':10}
                    ),
                html.Div(id="cust_bioreactors",
                    children=u'The custom number of bioreactors is {:20}.'.format(int(cust_BioReact))),
                html.Div(id="cust_output1",
                    children=u'The custom bioreactor cost is ${:20,.2f}.'.format(BioEquip_Cust)),
                html.Div(id="cust_output2",
                    children=u'The custom total bioreactor cost is ${:20,.2f}.'.format(BioEquip_Cust_total)),
                html.Div(id="cust_output3",
                    children=u'The custom fixed manufacturing cost is ${:20,.2f}.'.format(Fix_Manu_Cust_Cost)),
                html.Div(id="cust_output4",
                    children=u'The custom cost of media is ${:20,.2f} per liter.'.format(cust_Media_Cost)),
                html.Div(id="annmediacost_output",
                    children=u'The custom annual cost of media is ${:20,.2f}.'.format(cust_AnnMediaCost))])
                ], className="six columns",style={'marginBottom': 20}),
#         html.Div([ # Right Side: Some words
#             html.H1(children='Big Words #1',
#                    style={
#                     'textAlign': 'center'})
#             ], className="six columns"),
    html.Div([
        html.Div([
             html.Label('Custom Cost Scales',
                 style={'textAlign': 'center'}),
            # First Scale: Custom Bioreactor Working Volume
            html.Div([
                html.I("Adjust the working volume of the bioreactors.")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'bioreactslider',
                    min = (0.25 * BRWV),
                    max = (1000000),
                    value = cust_BRWV,
                    step=1.0,
                    marks={25000: "25,000 L"}
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="bioreactor_output",
                        children=u'The custom working volume of the bioreactors is set to {} L.'.format(cust_BRWV)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
            # Second Slider: Custom FGF2 Concentration (g/L) 
            html.Div([
                html.I("Adjust the g/L needed of FGF-2.")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'fgf2_gL_slider',
                    min = 0,
                    max = 2*max(FGF2Con),
                    value = cust_FGF2Con,
                    step=0.00001
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="cust_FGF2Con_output",
                        children=u'The concentration of FGF-2 is set to {} g/L.'.format(cust_FGF2Con)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
            # Slider 3: Custom FGF-2 Cost $/g
            html.Div([
                html.I("Adjust the $ per g of FGF-2.")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'fgf2_costg_slider',
                    min = 0,
                    max = 2*max(FGF2Cost),
                    value = cust_FGF2Cost,
                    step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="cust_FGF2Cost_output",
                        children=u'The custom cost of FGF-2 is set to $ {} per gram.'.format(cust_FGF2Cost)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
            # Slider 4: Achievable Cell Concentration (ACC; cell/mL)
            html.Div([
                html.I("Adjust the achievable cell concentration (cells/mL).")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'acc_slider',
                    min = float(min(ACC) / 2),
                    max = 2*max(ACC),
                    value = cust_ACC#,
                    #step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="acc_output",
                        children=u'The achievable cell concentration is set to {} cells/mL.'.format(cust_FGF2Cost)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
            # Slide 5: Custom Maturation Time (h; hours)
            html.Div([
                html.I("Adjust the cell maturation time (h).")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'mat_time_slider',
                    min = float(0),
                    max = 2*max(MatTime),
                    value = cust_MatTime,
                    step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="mat_time_output",
                        children=u'The cell maturation time is set to {} hours.'.format(cust_MatTime)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
             # Slide 6: Custom Hours per doubling (hours, h)
            html.Div([
                html.I("Adjust the custom hours per doubling of cells (h).")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'hr_doub_slider',
                    min = float(0.5 * min(d)),
                    max = float(2 * max(d)),
                    value = cust_hr_doub#,
                    #step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="hr_doub_output",
                        children=u'The custom hours per doubling of cells is set to {} hours.'.format(cust_hr_doub)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
             # Slide 7: Custom Glucose consumption rate per cell [Ug; (mol/(hr*cell))]
            html.Div([
                html.I("Adjust the custom Glucose consumption rate per cell (mol/(h*cell)).")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'ug_slider',
                    min = 104,
                    max = 826,
                    value = cust_Ug*10**13,
                    step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="Ug_output",
                        children=u'The custom Glucose consumption rate per cell is set to {} mol/(h*cell).'.format(cust_Ug)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
            # Slide 8: Custom Glucose concentration in basal media (mol/L)
            html.Div([
                html.I("Adjust the custom Glucose concentration in basal media (mol/L).")],
                style={'marginBottom': 10,'marginTop': 20}),
            html.Div([
                dcc.Slider(
                    id = 'GConInBM_slider',
                    min = float(0.0089),
                    max = float(0.0712),
                    value = cust_GConInBM,
                    step=0.0001
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                html.Div(id="GConInBM_output",
                        children=u'The custom Glucose concentration in basal media is set to {} mol/L.'.format(cust_GConInBM)
                        )],
                style={'marginBottom': 10,'marginTop': 10}),
        ], className="six columns")
        ])#, className="row"),
     ], className="row"),
# Bottom block: Logout Button and other things    
    html.Div([    
        dcc.LogoutButton(id="logout")],
        style={'marginBottom': 10,'marginTop': 10})
])

######## Begining of Callbacks #########

@app.callback(
    [Output('graph', 'figure'),
     Output('cust_bioreactors', 'children'),
     Output('cust_output1', 'children'),
     Output('cust_output2', 'children'),
     Output('cust_output3', 'children'),
     Output('cust_output4', 'children'),
     Output('cust_FGF2Cost_output','children'),
     Output('acc_output','children'),
     Output("annmediacost_output",'children')
    ],
    [Input('bioreactslider','value'),
     Input('fgf2_gL_slider','value'),
     Input('fgf2_costg_slider','value'),
     Input('acc_slider','value'),
     Input('mat_time_slider','value'),
     Input('hr_doub_slider','value'),
     Input('ug_slider','value'),
     Input('GConInBM_slider','value')
    ])

def update_figure(slider1,slider2,slider3,slider4,slider5,slider6,slider7,slider8):
    '''Function to update custom cost from 
    slider1 input. '''    
    # New Custom Variables from sliders
    new_cust_BRWV = slider1
    new_cust_FGF2Con = slider2
    new_cust_FGF2Cost = slider3
    new_cust_ACC = slider4
    new_cust_MatTime = slider5
    new_cust_hr_doub = slider6
    new_cust_Ug = slider7 / 10**13
    new_cust_GConInBM = slider8    
    # New Custom Media Cost Variables
    new_cust_GluCon_Mat = glucose_cons_in_mat(new_cust_BRWV,new_cust_ACC,new_cust_Ug,new_cust_MatTime)
    new_cust_GluCon_Growth = float(total_glu_consume_growth(growth_time(new_cust_hr_doub),
                                                            (new_cust_ACC * new_cust_Ug),new_cust_hr_doub))
    new_cust_GluInCharge = float(new_cust_BRWV * new_cust_GConInBM)
    new_cust_TotCluConBatch = new_cust_GluCon_Growth + new_cust_GluCon_Mat
    new_cust_MediaChargeBatch = new_cust_TotCluConBatch / new_cust_GluInCharge
    new_cust_Media_Vol = new_cust_BRWV * new_cust_MediaChargeBatch
    new_cust_BatchPerYear = AnnOpTime / (new_cust_MatTime + growth_time(new_cust_hr_doub))
    new_cust_CellMassBatch = cell_mass_per_batch(new_cust_BRWV,new_cust_ACC)
    new_cust_ACBM = new_cust_CellMassBatch * new_cust_BatchPerYear
    new_cust_BioReact = DesiredMassMeat / new_cust_ACBM
    new_cust_AnnBatches = new_cust_BioReact * new_cust_BatchPerYear
    new_BioEquip_Cust = new_cust_BioReact * tot_fixed_eq_costs
    new_BioEquip_Cust_total = new_BioEquip_Cust * 2
    new_Fix_Manu_Cust_Cost = new_BioEquip_Cust_total * FixManuCost_Factor
    new_cust_Media_Cost = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (new_cust_FGF2Con * new_cust_FGF2Cost)
    new_cust_AnnVolMedia = new_cust_Media_Vol * new_cust_AnnBatches
    new_cust_AnnMediaCost = new_cust_AnnVolMedia * new_cust_Media_Cost    
    # New Data lists 
    new_Costs_Bioequip = [BioEquip1,BioEquip2,BioEquip3,BioEquip4,new_BioEquip_Cust]
    new_Costs_BioEquipTotal = [BioEquip1_total,BioEquip2_total,BioEquip3_total,BioEquip4_total,new_BioEquip_Cust_total]
    new_Costs_Fixed_Manu = [Fix_Manu_Cost1,Fix_Manu_Cost2,Fix_Manu_Cost3,Fix_Manu_Cost4,new_Fix_Manu_Cust_Cost]
    new_AnnMediaCosts = [AnnMediaCost1,AnnMediaCost2,AnnMediaCost3,AnnMediaCost4,new_cust_AnnMediaCost]
    # Updated Figure 
    new_fig = go.Figure()    
    new_fig.add_trace(go.Bar(
        x=Scenarios,
        y=new_Costs_Bioequip,
        name='Bioreactor Costs',
        marker_color='indianred',
        offsetgroup=0,
        hovertemplate='Scenario: %{x}<br>Bioreactor Cost: %{y}<extra></extra>'
    ))
    new_fig.add_trace(go.Scatter(
        x=Scenarios,
        y=new_Costs_BioEquipTotal,
        name='Fixed Total Bioreactor Costs',
        marker_color='#FFA505',
        mode="markers",
        #offsetgroup=0,
        #base=new_Costs_Bioequip,
        hovertemplate='Scenario: %{x}<br>Fixed Total Bioreactor Cost: %{y}<extra></extra>'
    ))
    new_fig.add_trace(go.Bar(
        x=Scenarios,
        y=Costs_Fixed_Manu,
        name='Fixed Manufacturing Cost',
        marker_color='firebrick',
        offsetgroup=1,
        hovertemplate='Scenario: %{x}<br>Fixed Manufacturing Cost: %{y}<extra></extra>'
    ))
    new_fig.add_trace(go.Bar(
        x=Scenarios,
        y=new_AnnMediaCosts,
        name='Annual Media Cost',
        marker_color='teal',
        offsetgroup=2,
        hovertemplate='Scenario: %{x}<br>Annual Media Cost: %{y}<extra></extra>'
    ))    
    new_fig.update_layout(xaxis_tickangle=45, yaxis_type="log", yaxis_title="US Dollars ($)")   
    return [new_fig, 
            u'The custom number of bioreactors is {:20}.'.format(int(new_cust_BioReact)),
            u'The custom bioreactor cost is ${:20,.2f}.'.format(new_BioEquip_Cust),
            u'The custom total bioreactor cost is ${:20,.2f}.'.format(new_BioEquip_Cust_total),
            u'The custom fixed manufacturing cost is ${:20,.2f}.'.format(new_Fix_Manu_Cust_Cost),
            u'The custom cost of media is ${:20,.2f} per liter.'.format(new_cust_Media_Cost),
            u'The custom cost of FGF-2 is set to $ {:20,.2f} per gram.'.format(new_cust_FGF2Cost),
            u'The achievable cell concentration is set to {:20,.2f} cells/mL.'.format(slider4),
            u'The custom annual cost of media is ${:20,.2f}.'.format(new_cust_AnnMediaCost)
           ]

##### Bioreactor Slider Chained Callbacks #######

@app.callback(
    Output('bioreactor_output', 'children'),
    [Input('bioreactslider','value')])

def update_scale1_output1(slider1_input):
    bio_output = slider1_input
    if bio_output > 25000:
        return u'The custom working volume of the bioreactors is set to {} L. Bioreactors used for animal cell culture with working volumes greater than 25,000 L are custom bioreactors and as of 2019 are not commercially available.'.format(bio_output)
    else:
        return u'The custom working volume of the bioreactors is set to {} L.'.format(bio_output)

##### FGF2 Conc Slider Chained Callbacks #######

@app.callback(
    Output('cust_FGF2Con_output', 'children'),
    [Input('fgf2_gL_slider','value')])

def update_scale2_output1(slider2_input):
    if slider2_input > 2*max(FGF2Con):
        upd_cust_FGF2Con = 2*max(FGF2Con)
    else:
        upd_cust_FGF2Con = slider2_input
    return u'The concentration of FGF-2 is set to {} g/L.'.format(upd_cust_FGF2Con)


#### App launching functions ######

port = 8050 

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))
    
application = app.server

if __name__ == '__main__':
    Timer(0, open_browser).start();
    app.run_server(debug=True, port=port)
