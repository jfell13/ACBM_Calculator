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

####### Fixed Constants #########
BRWV = float(20000) # Bioreactor working volume (L)
FGF2MM = float(24000)
FixManuCost_Factor = float(0.15)
BRUC = float(50000) # Bioreactor Unit Cost = $50,000 per reactor in m^3
Adj_BioR_valu = float(1.29) # Adjusted Bioreactor value
BV = float(20.0) # Bioreactor volume (m^3)
BioRScF = float(0.60) # Bioreactor Scale Factor
BMC = float(3.12) # Basal Media Cost
TGFB = float(3236000*0.000002)
Transferrin = float(400 * 0.0107)
Insulin = float(340 * 0.0194)
NaSel = float(0.10 * 0.0000140)
NaHCO3 = float(0.543 * 0.01)
AA2D = float(7.84 * 0.0640)
AnnOpTime = 8760 # Annual Operating Time
AveCellDensity = 1060 # Average Single Cell Density (kg/m^3)
AveCellVol = float(0.000000000000005) # Average Single Cell volume (m^3 per cell)
DesiredMassMeat = float(119000000) # Desired Mass of Meat Produced 
tot_fixed_eq_costs = Adj_BioR_valu * BRUC * (BV**BioRScF)

###### Custom Starting Variables  #########
cust_BRWV = float(20000)
cust_FGF2Con = float(0.0001)
cust_FGF2Cost = float(4010000)
cust_Ug = float(0.0000000000000413)
cust_GConInBM = float(0.0178)
cust_MatTime = float(24)
cust_hr_doub = float(8.0)
cust_ACC = float(10000000)

##### Media Related variables per scenario ########
ACC = [float(10000000),float(95000000),float(95000000),float(200000000)] # Achievable cell concentration cells/mL
Ug = [float(0.000000000000413),float(0.000000000000207),float(0.000000000000207),float(0.0000000000000413)] 
# Ug = Glu. cons. rate per cell (mol/ h cell)
MatTime = [240, 156, 156, 24] # Maturation Time (h)
d = [24.0, 16.0, 16.0, 8.0] # Hours per doubling (h)
FGF2Con = [float(0.0001),float(0.00005),float(0.00005),float(0.0)] # FGF-2 conc. (g/L)
FGF2Cost = [float(4010000),float(2010000),float(0),float(0)] # FGF-2 cost (USD/g)
GConInBM = [float(0.0178),float(0.0267),float(0.0267),float(0.0356)] # Glucose concentration in basal media (mol/L)

###### Functions for Calculating other variables ########

def growth_time(doubling_time):
    growth = float((np.log(100) / np.log(2)) * doubling_time)
    return growth

def cell_mass_per_batch(Vol,CellCount):
    mass_per = float(Vol * AveCellDensity * AveCellVol * 1000 * CellCount)
    return mass_per

def total_glu_consume_growth(Mature_Time, scenario, doubling):
    glu_consumed = []
    for i in range(0,int(Mature_Time / doubling) + 1):
        glu_consumed.append(float((2**(i)) * scenario * doubling))
    return sum(glu_consumed)

def glucose_cons_in_mat(Vol,CellCount,ConsRate,MatureTime):
    consumed_in_mat = float(Vol * CellCount * 1000 * ConsRate * MatureTime)
    return consumed_in_mat

#def something():

# Total Glucose consumed in Maturation and Growth Phases
GluConInMatPhase1 = glucose_cons_in_mat(BRWV,ACC[0],Ug[0],MatTime[0])
GluConInMatPhase2 = glucose_cons_in_mat(BRWV,ACC[1],Ug[1],MatTime[1])
GluConInMatPhase3 = glucose_cons_in_mat(BRWV,ACC[2],Ug[2],MatTime[2])
GluConInMatPhase4 = glucose_cons_in_mat(BRWV,ACC[3],Ug[3],MatTime[3])
cust_GluCon_Mat = glucose_cons_in_mat(cust_BRWV,cust_ACC,cust_Ug,cust_MatTime)

GluConInGrowthPhase1 = float(total_glu_consume_growth(growth_time(d[0]),(ACC[0] * Ug[0]),d[0]))
GluConInGrowthPhase2 = float(total_glu_consume_growth(growth_time(d[1]),(ACC[1] * Ug[1]),d[1]))
GluConInGrowthPhase3 = float(total_glu_consume_growth(growth_time(d[2]),(ACC[2] * Ug[2]),d[2]))
GluConInGrowthPhase4 = float(total_glu_consume_growth(growth_time(d[3]),(ACC[3] * Ug[3]),d[3]))
cust_GluCon_Growth = float(total_glu_consume_growth(growth_time(cust_hr_doub),(cust_ACC * cust_Ug),cust_hr_doub))
# Total Glucose in Charge (mol)
GluInCharge1 = float(BRWV * GConInBM[0])
GluInCharge2 = float(BRWV * GConInBM[1])
GluInCharge3 = float(BRWV * GConInBM[2])
GluInCharge4 = float(BRWV * GConInBM[3])
cust_GluInCharge = float(cust_BRWV * cust_GConInBM)
# Total Glucose Consumed per Batch (mol)
TotGluConBatch1 = GluConInGrowthPhase1 + GluConInMatPhase1
TotGluConBatch2 = GluConInGrowthPhase2 + GluConInMatPhase2
TotGluConBatch3 = GluConInGrowthPhase3 + GluConInMatPhase3
TotGluConBatch4 = GluConInGrowthPhase4 + GluConInMatPhase4
cust_TotCluConBatch = cust_GluCon_Growth + cust_GluCon_Mat
# Media Charges per batch (mol/mol)
MediaChargeBatch1 = TotGluConBatch1 / GluInCharge1
MediaChargeBatch2 = TotGluConBatch2 / GluInCharge2
MediaChargeBatch3 = TotGluConBatch3 / GluInCharge3
MediaChargeBatch4 = TotGluConBatch4 / GluInCharge4
cust_MediaChargeBatch = cust_TotCluConBatch / cust_GluInCharge
# Volume of Media per Batch (L)
Media_Vol1 = BRWV * MediaChargeBatch1
Media_Vol2 = BRWV * MediaChargeBatch2
Media_Vol3 = BRWV * MediaChargeBatch3
Media_Vol4 = BRWV * MediaChargeBatch4
cust_Media_Vol = cust_BRWV * cust_MediaChargeBatch
# Bacthes per Year per BioReactor
BatchPerYear1 = AnnOpTime / (MatTime[0] + growth_time(d[0]))
BatchPerYear2 = AnnOpTime / (MatTime[1] + growth_time(d[1]))
BatchPerYear3 = AnnOpTime / (MatTime[2] + growth_time(d[2]))
BatchPerYear4 = AnnOpTime / (MatTime[3] + growth_time(d[3]))
cust_BatchPerYear = AnnOpTime / (cust_MatTime + growth_time(cust_hr_doub))

CellMassBatch1 = cell_mass_per_batch(BRWV,ACC[0])
CellMassBatch2 = cell_mass_per_batch(BRWV,ACC[1])
CellMassBatch3 = cell_mass_per_batch(BRWV,ACC[2])
CellMassBatch4 = cell_mass_per_batch(BRWV,ACC[3])
cust_CellMassBatch = cell_mass_per_batch(cust_BRWV,cust_ACC)

ACBM1 = CellMassBatch1 * BatchPerYear1
ACBM2 = CellMassBatch2 * BatchPerYear2
ACBM3 = CellMassBatch3 * BatchPerYear3
ACBM4 = CellMassBatch4 * BatchPerYear4
cust_ACBM = cust_CellMassBatch * cust_BatchPerYear
# Calculated BioReactor numbers 
BioReact1 = DesiredMassMeat / ACBM1
BioReact2 = DesiredMassMeat / ACBM2
BioReact3 = DesiredMassMeat / ACBM3
BioReact4 = DesiredMassMeat / ACBM4
cust_BioReact = DesiredMassMeat / cust_ACBM

AnnBatches1 = BioReact1 * BatchPerYear1
AnnBatches2 = BioReact2 * BatchPerYear2
AnnBatches3 = BioReact3 * BatchPerYear3
AnnBatches4 = BioReact4 * BatchPerYear4
cust_AnnBatches = cust_BioReact * cust_BatchPerYear

BIOREACTORS = [BioReact1, BioReact2, BioReact3, BioReact4] # Bioreactor numbers
# Costs for BioReactors
BioEquip1 = BIOREACTORS[0] * tot_fixed_eq_costs 
BioEquip2 = BIOREACTORS[1] * tot_fixed_eq_costs 
BioEquip3 = BIOREACTORS[2] * tot_fixed_eq_costs 
BioEquip4 = BIOREACTORS[3] * tot_fixed_eq_costs 
BioEquip_Cust = cust_BioReact * tot_fixed_eq_costs
# Total Bioequpiment costs
BioEquip1_total = BioEquip1 * 2
BioEquip2_total = BioEquip2 * 2 
BioEquip3_total = BioEquip3 * 2 
BioEquip4_total = BioEquip4 * 2 
BioEquip_Cust_total = BioEquip_Cust * 2
# Fixed Manufacturing Costs
Fix_Manu_Cost1 = BioEquip1_total * FixManuCost_Factor
Fix_Manu_Cost2 = BioEquip2_total * FixManuCost_Factor
Fix_Manu_Cost3 = BioEquip3_total * FixManuCost_Factor
Fix_Manu_Cost4 = BioEquip4_total * FixManuCost_Factor
Fix_Manu_Cust_Cost = BioEquip_Cust_total * FixManuCost_Factor
# Cost of Media per L
Media_Cost1 = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (FGF2Con[0]*FGF2Cost[0])
Media_Cost2 = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (FGF2Con[1]*FGF2Cost[1])
Media_Cost3 = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (FGF2Con[2]*FGF2Cost[2])
Media_Cost4 = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (FGF2Con[3]*FGF2Cost[3])
cust_Media_Cost = BMC + TGFB + Transferrin + Insulin + NaSel + NaHCO3 + AA2D + (cust_FGF2Con * cust_FGF2Cost)
# Annual Volume of Media
AnnVolMedia1 = Media_Vol1 * AnnBatches1
AnnVolMedia2 = Media_Vol2* AnnBatches2
AnnVolMedia3 = Media_Vol3 * AnnBatches3
AnnVolMedia4 = Media_Vol4 * AnnBatches4
cust_AnnVolMedia = cust_Media_Vol * cust_AnnBatches
# Total Annual Cost of Media
AnnMediaCost1 = AnnVolMedia1 * Media_Cost1
AnnMediaCost2 = AnnVolMedia2 * Media_Cost2
AnnMediaCost3 = AnnVolMedia3 * Media_Cost3
AnnMediaCost4 = AnnVolMedia4 * Media_Cost4
cust_AnnMediaCost = cust_AnnVolMedia * cust_Media_Cost

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
    name='Bioequipment Costs',
    marker_color='indianred',
    offsetgroup=0,
    hovertemplate='Scenario: %{x}<br>Variable Cost: %{y}<extra></extra>'
))

fig.add_trace(go.Scatter(
    x=Scenarios,
    y=Costs_BioEquipTotal,
    name='Fixed Total Bioequipment Costs',
    marker_color='#FFA505',
    mode="markers",
    #offsetgroup=0,
    #base=Costs_Bioequip,
    hovertemplate='Scenario: %{x}<br>Fixed Cost: %{y}<extra></extra>'
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

fig.update_layout(xaxis_tickangle=45)

# Cost3_trace = go.Bar(y=Cost3,
#                          mode="lines+markers",
#                          name="Scenario 3",
#                          marker = dict(color='royalblue'),
#                          line = dict(color='royalblue', width=2),
#                          hovertemplate='Scenario 3<br>Cost: %{y}<extra></extra>')
# Cost4_trace = go.Bar(y=Cost4,
#                          mode="lines+markers",
#                          name="Scenario 4",
#                          marker = dict(color='teal'),
#                          line = dict(color='teal', width=2),
#                          hovertemplate='Scenario 4<br>Cost: %{y}<extra></extra>')

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
            html.Div([
                dcc.Graph( # Output of Graphs and Custom Values
                    id='graph',
                    figure=fig,
                    style={'padding':10}
                    ),
                html.Div(id="cust_bioreactors",
                    children=u'The custom number of bioreactors is {}.'.format(int(cust_BioReact))),
                html.Div(id="cust_output1",
                    children=u'The custom bioequpiment cost is ${}.'.format(round(BioEquip_Cust,2))),
                html.Div(id="cust_output2",
                    children=u'The custom total bioequpiment cost is ${}.'.format(round(BioEquip_Cust_total,2))),
                html.Div(id="cust_output3",
                    children=u'The custom fixed manufacturing cost is ${}.'.format(round(Fix_Manu_Cust_Cost,2))),
                html.Div(id="cust_output4",
                    children=u'The custom cost of media is ${} per liter.'.format(round(cust_Media_Cost,2))),
                html.Div(id="annmediacost_output",
                    children=u'The custom annual cost of media is ${}.'.format(round(cust_AnnMediaCost,2)))])
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
                    max = (2 * BRWV),
                    value = cust_BRWV,
                    step=1.0
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                dcc.Input(id="bioreact", 
                          type='number', 
                          value = cust_BRWV,
                          step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                dcc.Input(id="fgf2_gL", 
                          type='number',
                          value = cust_FGF2Con,
                          step=0.00001
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                dcc.Input(id="fgf2_costg", 
                          type='number',
                          value = cust_FGF2Cost,
                          step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                dcc.Input(id="acc_input", 
                          type='number',
                          value = cust_ACC#,
                          #step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
            html.Div([
                html.Div(id="acc_output",
                        children=u'The achievable cell concentration is set to {} cells.'.format(cust_FGF2Cost)
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
                dcc.Input(id="mat_time_input", 
                          type='number',
                          value = cust_MatTime#,
                          #step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                dcc.Input(id="hr_doub_input", 
                          type='number',
                          value = cust_hr_doub,
                          step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                    min = float(0.00000000000002065),
                    max = float(2 * max(Ug)),
                    value = cust_Ug#,
                    #step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                dcc.Input(id="ug_input", 
                          type='number',
                          value = cust_Ug#,
                          #step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
                    min = float(0.0178 / 2),
                    max = float(2 * max(GConInBM)),
                    value = cust_GConInBM#,
                    #step=1
                )],
                style={'marginBottom': 20,'marginTop': 20}),
            html.Div([
                dcc.Input(id="GConInBM_input", 
                          type='number',
                          value = cust_GConInBM#,
                          #step=1
                         )],
                style={'marginBottom': 10,'marginTop': 10}),
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
    new_cust_Ug = slider7
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
        name='Bioequipment Costs',
        marker_color='indianred',
        offsetgroup=0,
        hovertemplate='Scenario: %{x}<br>Bioequipment Cost: %{y}<extra></extra>'
    ))
    new_fig.add_trace(go.Scatter(
        x=Scenarios,
        y=new_Costs_BioEquipTotal,
        name='Fixed Total Bioequipment Costs',
        marker_color='#FFA505',
        mode="markers",
        #offsetgroup=0,
        #base=new_Costs_Bioequip,
        hovertemplate='Scenario: %{x}<br>Fixed Total Bioequipment Cost: %{y}<extra></extra>'
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
    new_fig.update_layout(xaxis_tickangle=45)   
    return [new_fig, 
            u'The custom number of bioreactors is {}.'.format(int(new_cust_BioReact)),
            u'The custom bioequpiment cost is ${}.'.format(round(new_BioEquip_Cust,2)),
            u'The custom total bioequpiment cost is ${}.'.format(round(new_BioEquip_Cust_total,2)),
            u'The custom fixed manufacturing cost is ${}.'.format(round(new_Fix_Manu_Cust_Cost,2)),
            u'The custom cost of media is ${} per liter.'.format(round(new_cust_Media_Cost,2)),
            u'The custom cost of FGF-2 is set to $ {} per gram.'.format(new_cust_FGF2Cost),
            u'The achievable cell concentration is set to {} cells.'.format(slider4),
            u'The custom annual cost of media is ${}.'.format(round(new_cust_AnnMediaCost,2))
           ]

##### Bioreactor Slider Chained Callbacks #######

@app.callback(
    Output('bioreactor_output', 'children'),
    [Input('bioreactslider','value')])

def update_scale1_output1(slider1_input):
    if slider1_input > 2 * BRWV:
        bio_output = 2 * BRWV
    else:
        bio_output = slider1_input
    return u'The custom working volume of the bioreactors is set to {}.'.format(bio_output)

@app.callback(
    Output('bioreactslider','value'),
    [Input('bioreact', 'value')])
    
def update_scale1(bioreact_input):
    if bioreact_input == None:
        bioreact = cust_BRWV
    else:
        if bioreact_input > 2 * BRWV:
            bioreact = 2 * BRWV
        else:
            bioreact = bioreact_input
    return bioreact

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

@app.callback(
    Output('fgf2_gL_slider','value'),
    [Input('fgf2_gL', 'value')])
    
def update_scale2(input2):
    if input2 == None:
        fgfgL = 0
    else:
        if input2 > 2*max(FGF2Con):
            fgfgL = 2*max(FGF2Con)
        else:
            fgfgL = input2
    return fgfgL

#### App launching functions ######

port = 8050 

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))
    
application = app.server

if __name__ == '__main__':
    Timer(0, open_browser).start();
    app.run_server(debug=True, port=port)
