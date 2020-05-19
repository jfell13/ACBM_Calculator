from constants import *
from bioreactor_and_media import *

def total_O2_consume_growth(Mature_Time, starting_cell_count, doubling):
    '''starting_cell_count = ACC'''
    O2_consumed = []
    for i in range(0,int(Mature_Time / doubling) + 1):
        curr_cell_count = float(2**(i) * starting_cell_count)
        curr_o2_uptake = curr_cell_count * oxygen_comsump
        O2_consumed.append(curr_o2_uptake * doubling)
    return sum(O2_consumed)

## O2 Consumed In Maturation ##

O2_cons_in_mat1 = float((BRWV * ACC[0] * 1000) * MatTime[0] * oxygen_comsump)
O2_cons_in_mat2 = float((BRWV * ACC[1] * 1000) * MatTime[1] * oxygen_comsump)
O2_cons_in_mat3 = float((BRWV * ACC[2] * 1000) * MatTime[2] * oxygen_comsump)
O2_cons_in_mat4 = float((BRWV * ACC[3] * 1000) * MatTime[3] * oxygen_comsump)
cust_O2_cons_in_mat = float((cust_BRWV * cust_ACC * 1000) * cust_MatTime * oxygen_comsump)

## Initial O2 per batch

initial_O2_batch1 = float(((MediaChargeBatch1 * BRWV) * media_Density * perc_O2_initial_charge) / mm_O2)
initial_O2_batch2 = float(((MediaChargeBatch2 * BRWV) * media_Density * perc_O2_initial_charge) / mm_O2)
initial_O2_batch3 = float(((MediaChargeBatch3 * BRWV) * media_Density * perc_O2_initial_charge) / mm_O2)
initial_O2_batch4 = float(((MediaChargeBatch4 * BRWV) * media_Density * perc_O2_initial_charge) / mm_O2)
cust_initial_O2_batch = float(((cust_MediaChargeBatch * cust_BRWV) * media_Density * perc_O2_initial_charge) / mm_O2)

## Total O2 Consumed in Growth

total_O2_cons_growth1 = float(total_O2_consume_growth(growth_time(d[0]),ACC[0],d[0]))
total_O2_cons_growth2 = float(total_O2_consume_growth(growth_time(d[1]),ACC[1],d[1]))
total_O2_cons_growth3 = float(total_O2_consume_growth(growth_time(d[2]),ACC[2],d[2]))
total_O2_cons_growth4 = float(total_O2_consume_growth(growth_time(d[3]),ACC[3],d[3]))
cust_total_O2_cons_growth = float(total_O2_consume_growth(growth_time(cust_hr_doub),cust_ACC,cust_hr_doub))

## O2 Consumed per batch

O2_consum_batch1 = float(total_O2_cons_growth1 + initial_O2_batch1 + O2_cons_in_mat1)
O2_consum_batch2 = float(total_O2_cons_growth2 + initial_O2_batch2 + O2_cons_in_mat2)
O2_consum_batch3 = float(total_O2_cons_growth3 + initial_O2_batch3 + O2_cons_in_mat3)
O2_consum_batch4 = float(total_O2_cons_growth4 + initial_O2_batch4 + O2_cons_in_mat4)
cust_O2_consum_batch = float(cust_total_O2_cons_growth + cust_initial_O2_batch + cust_O2_cons_in_mat)

## Annual O2 Consumption

Ann_O2_Consum1 = float((O2_consum_batch1 * mm_O2 * AnnBatches1)/1000)
Ann_O2_Consum2 = float((O2_consum_batch2 * mm_O2 * AnnBatches2)/1000)
Ann_O2_Consum3 = float((O2_consum_batch3 * mm_O2 * AnnBatches3)/1000)
Ann_O2_Consum4 = float((O2_consum_batch4 * mm_O2 * AnnBatches4)/1000)
cust_Ann_O2_Consum = float((cust_O2_consum_batch * mm_O2 * cust_AnnBatches)/1000)

## Annual O2 Cost

Ann_O2_Cost1 = float(Ann_O2_Consum1 * cost_O2)
Ann_O2_Cost2 = float(Ann_O2_Consum2 * cost_O2)
Ann_O2_Cost3 = float(Ann_O2_Consum3 * cost_O2)
Ann_O2_Cost4 = float(Ann_O2_Consum4 * cost_O2)
cust_Ann_O2_Cost = float(cust_Ann_O2_Consum * cost_O2)