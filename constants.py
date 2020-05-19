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
DesiredMassMeat = float(121000000) # Desired Mass of Meat Produced in kg
tot_fixed_eq_costs = Adj_BioR_valu * BRUC * (BV**BioRScF)
oxygen_comsump = float(0.0000000000000180) # mol/(h*cell)
mm_O2 = float(0.032) # kg/mol
media_Density = float(1.00) # kg/L
perc_O2_initial_charge = float(0.02) # %ww
cost_O2 = float(40.00) # USD/ton
natural_gas_cost = float(4.17) # $ per 1000 ft^3
natural_gas = float(1.42) # cents per kWh
boiler_ener_eff = float(0.85) # Percentage
desired_Temp = float(37.00) # Desired tempersture in C
starting_Water_temp = float(20.00) # Starting water temp in C
water_spec_Heat = float(0.0016) # Specific Heat of Water kWh/(kg*C)
heat_release_O2 = float(0.13) # Heat released per O2 consumed kWh
heater_eff = float(1.00) #
water_cooler_eff = float(1.00) #
ACBM_cooler_eff = float(1.00)
ACBM_cool_temp = float(4.00) # Temp of cooled ACBM meat
ACBM_spec_heat = float(0.000622) # Specific heat of ACBM
prod_worker_wage = float(13.68) # $ per hour
Labor_Cost_Corr_Fact = float(1 * 1.2 * 0.8 * 1.5 * 1.4 * 1.25)
Process_Water_Cost = float(0.63) # $/m^3
Waste_Water_Cost = float(0.51) # $/m^3
Oxidation_Water_Cost = float(0.57) # $/m^3

###### Custom Starting Variables  #########
cust_BRWV = float(20000)
cust_FGF2Con = float(0.0001)
cust_FGF2Cost = float(4010000)
cust_Ug = 4.13E-13
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