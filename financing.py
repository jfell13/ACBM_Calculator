import math
from constants import *
from bioreactor_and_media import *
from oxygen import *
from energy import *
from labor import *
from non_electric import *

Economic_Life = 20 # Years
Cost_of_Equity = 0.15 # % per Y
Debt_Interest_Rate = 0.05 # % per Y
Debt_Ratio = 0.90

cap_rec_fac_num = (Cost_of_Equity * (1 + Cost_of_Equity)**Economic_Life)
cap_rec_fac_denom = ((1 + Cost_of_Equity)**Economic_Life - 1)
cap_rec_fac = cap_rec_fac_num / cap_rec_fac_denom

debt_rec_fac_num = (Debt_Interest_Rate * (1 + Debt_Interest_Rate)**Economic_Life)
debt_rec_fac_denom = ((1 + Debt_Interest_Rate)**Economic_Life - 1)
debt_rec_fac = debt_rec_fac_num / debt_rec_fac_denom

def Ann_Debt_Payment(cap_exp):
    Ann_Debt_Payment = float(cap_exp * Debt_Ratio * debt_rec_fac)
    return float(Ann_Debt_Payment)

def Ann_Equity_Recov(cap_exp): 
    Ann_Equity_Recov = float(cap_rec_fac * cap_exp * (1 - Debt_Ratio))
    return Ann_Equity_Recov

def total_ann_payment_cap_exp(Ann_Debt_Payment,Ann_Equity_Recov):
    total_ann_payment_cap_exp = float(Ann_Debt_Payment + Ann_Equity_Recov) # USD per Y
    return total_ann_payment_cap_exp

annual_debt = [Ann_Debt_Payment(Fix_Manu_Cost1),
               Ann_Debt_Payment(Fix_Manu_Cost2),
               Ann_Debt_Payment(Fix_Manu_Cost3),
               Ann_Debt_Payment(Fix_Manu_Cost4),
               Ann_Debt_Payment(Fix_Manu_Cust_Cost)]

annual_equity = [Ann_Equity_Recov(Fix_Manu_Cost1),
               Ann_Equity_Recov(Fix_Manu_Cost2),
               Ann_Equity_Recov(Fix_Manu_Cost3),
               Ann_Equity_Recov(Fix_Manu_Cost4),
               Ann_Equity_Recov(Fix_Manu_Cust_Cost)]

total_ann_payment = [total_ann_payment_cap_exp(annual_debt[0],annual_equity[0]),
                    total_ann_payment_cap_exp(annual_debt[1],annual_equity[1]),
                    total_ann_payment_cap_exp(annual_debt[2],annual_equity[2]),
                    total_ann_payment_cap_exp(annual_debt[3],annual_equity[3]),
                    total_ann_payment_cap_exp(annual_debt[4],annual_equity[4])]

cap_expend_with_debt_equity = [total_ann_payment[0]*Economic_Life,
                              total_ann_payment[1]*Economic_Life,
                              total_ann_payment[2]*Economic_Life,
                              total_ann_payment[3]*Economic_Life,
                              total_ann_payment[4]*Economic_Life]

###### Final Finance Values

Min_Ann_Op_Cost1 = float(Fix_Manu_Cost1 + AnnMediaCost1 + Ann_O2_Cost1 + Elect_Cost1 + Ann_Labor_Cost1 + Ann_Water_Cost1)
Min_Ann_Op_Cost2 = float(Fix_Manu_Cost2 + AnnMediaCost2 + Ann_O2_Cost2 + Elect_Cost2 + Ann_Labor_Cost2 + Ann_Water_Cost2)
Min_Ann_Op_Cost3 = float(Fix_Manu_Cost3 + AnnMediaCost3 + Ann_O2_Cost3 + Elect_Cost3 + Ann_Labor_Cost3 + Ann_Water_Cost3)
Min_Ann_Op_Cost4 = float(Fix_Manu_Cost4 + AnnMediaCost4 + Ann_O2_Cost4 + Elect_Cost4 + Ann_Labor_Cost4 + Ann_Water_Cost4)
cust_Min_Ann_Op_Cost = float(Fix_Manu_Cust_Cost + cust_AnnMediaCost + cust_Ann_O2_Cost + cust_Elect_Cost + cust_Ann_Labor_Cost + cust_Ann_Water_Cost)

Min_ACBM_tomeet_Exp1 = float(Min_Ann_Op_Cost1 / DesiredMassMeat)
Min_ACBM_tomeet_Exp2 = float(Min_Ann_Op_Cost2 / DesiredMassMeat)
Min_ACBM_tomeet_Exp3 = float(Min_Ann_Op_Cost3 / DesiredMassMeat)
Min_ACBM_tomeet_Exp4 = float(Min_Ann_Op_Cost4 / DesiredMassMeat)
cust_Min_ACBM_tomeet_Exp = float(cust_Min_Ann_Op_Cost / DesiredMassMeat)

Min_Ann_Cap_Op_Expend1 = (BioEquip1_total / Economic_Life) + Min_Ann_Op_Cost1
Min_Ann_Cap_Op_Expend2 = (BioEquip2_total / Economic_Life) + Min_Ann_Op_Cost2
Min_Ann_Cap_Op_Expend3 = (BioEquip3_total / Economic_Life) + Min_Ann_Op_Cost3
Min_Ann_Cap_Op_Expend4 = (BioEquip4_total / Economic_Life) + Min_Ann_Op_Cost4
cust_Min_Ann_Cap_Op_Expend = (BioEquip_Cust_total / Economic_Life) + cust_Min_Ann_Op_Cost

Min_ACBM_Price1 = float(Min_Ann_Cap_Op_Expend1 / DesiredMassMeat)
Min_ACBM_Price2 = float(Min_Ann_Cap_Op_Expend2 / DesiredMassMeat)
Min_ACBM_Price3 = float(Min_Ann_Cap_Op_Expend3 / DesiredMassMeat)
Min_ACBM_Price4 = float(Min_Ann_Cap_Op_Expend4 / DesiredMassMeat)
cust_Min_ACBM_Price = float(cust_Min_Ann_Cap_Op_Expend / DesiredMassMeat)
