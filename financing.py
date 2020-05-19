from constants import *
from bioreactor_and_media import *

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