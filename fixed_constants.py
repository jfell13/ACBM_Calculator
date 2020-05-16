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