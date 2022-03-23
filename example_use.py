import json
import pandas as pd
import re
import time
from import_ecm_results import import_ecm_results
from import_ecm_results import import_ecm_results_v1

# because _all_ ecms in ecm_results_1-1.json have the fuel type keys _v1 of the
# import function could be used.  This is done here only as an example to show
# how much faster it is to have a consistent data structure than to have to
# test for a possible fuel type.

#ecm_1 = import_ecm_results_v1("./Results_Files_3/ecm_results_1-1.json")
ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
#ecm_2 = import_ecm_results("./Results_Files_3/ecm_results_2.json")
#ecm_3 = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")
#ecm_4 = import_ecm_results("ecm_results_4.json")

print(ecm_1)
#print(ecm_2)
#print(ecm_3)
#print(ecm_4)


# NOTE: There is no rows in the following.  In the original work there would be
# output for this combination and the value set to 0.  In the current version of
# what @dewittpe has built this row is omitted from the output becuase there is
# no information to start with.
ecm_1[(ecm_1.region == "TRE") & (ecm_1.building_class == "Residential") & (ecm_1.end_use2 == "Other") & (ecm_1.fuel_type2 == "Oil")]

# To Reproduce ecm_results_1-1.csv we need only aggregate the data with four
# different groupby calls.

a0 = ecm_1\
        .groupby(['emf_string', 'year'])\
        .agg(value=('value','sum'))

a1 = ecm_1\
        .groupby(['emf_string', 'building_class', 'year'])\
        .agg(value=('value','sum'))

a2 = ecm_1\
        .groupby(['emf_string', 'building_class', 'end_use2', 'year'])\
        .agg(value=('value','sum'))

a3_0 = ecm_1[ecm_1.variable == "Avoided CO\u2082 Emissions (MMTons)"]\
        .groupby(['emf_string', 'building_class', 'end_use2', 'direct_fuel', 'year'])\
        .agg(value=('value','sum'))

a3_1 = ecm_1[ecm_1.variable == "Energy Savings (MMBtu)"]\
        .groupby(['emf_string', 'building_class', 'end_use2', 'fuel_type2', 'year'])\
        .agg(value=('value','sum'))

a3_2 = ecm_1[ecm_1.variable == "Energy Savings (MMBtu)"]\
        .groupby(['emf_string', 'building_class', 'fuel_type2', 'year'])\
        .agg(value=('value','sum'))

a3_3 = ecm_1[ecm_1.variable == "Energy Savings (MMBtu)"]\
        .groupby(['emf_string', 'fuel_type2', 'year'])\
        .agg(value=('value','sum'))

a0.reset_index(inplace = True)
a1.reset_index(inplace = True)
a2.reset_index(inplace = True)
a3_0.reset_index(inplace = True)
a3_1.reset_index(inplace = True)
a3_2.reset_index(inplace = True)
a3_3.reset_index(inplace = True)

# A multiplicative factor for energy savings
a3_1.value *= 1.05505585262e-9
a3_2.value *= 1.05505585262e-9
a3_3.value *= 1.05505585262e-9

a1.emf_string = a1.emf_string + "|" + a1.building_class
a2.emf_string = a2.emf_string + "|" + a2.building_class + "|" + a2.end_use2
a3_0.emf_string = a3_0.emf_string + "|" + a3_0.building_class + "|" + a3_0.end_use2 + "|" + a3_0.direct_fuel
a3_1.emf_string = a3_1.emf_string + "|" + a3_1.building_class + "|" + a3_1.end_use2 + "|" + a3_1.fuel_type2
a3_2.emf_string = a3_2.emf_string + "|" + a3_2.building_class + "|" + a3_2.fuel_type2
a3_3.emf_string = a3_3.emf_string + "|" + a3_3.fuel_type2

# one date frame
a = pd.concat([
            a0[["emf_string", "year", "value"]],
            a1[["emf_string", "year", "value"]],
            a2[["emf_string", "year", "value"]],
            a3_0[["emf_string", "year", "value"]],
            a3_1[["emf_string", "year", "value"]],
            a3_2[["emf_string", "year", "value"]],
            a3_3[["emf_string", "year", "value"]]
        ])
a = a.pivot(index = ["emf_string"], columns = ["year"], values = ["value"])
a.columns = a.columns.droplevel(0)
a.reset_index(inplace = True)

a

a.loc[a.emf_string == "BASN*Emissions|CO2|Energy|Demand|Buildings", ["2025", "2030"]]
a.loc[a.emf_string == "BASN*Final Energy|Buildings", ["2025", "2030"]]

a.to_csv("a.csv")

#BASN*Emissions|CO2|Energy|Demand|Buildings                                 , -0.16753753268025123    , -0.46469413903669343    , -0.6913137196346189    , -0.5114296223466639     , -0.3993793859084158     , -0.4211963089474491
#BASN*Final Energy|Buildings                                                , 0.004836432124608101    , 0.014637963363622889    , 0.027477157714066724   , 0.04329876010317799     , 0.06092553282306126     , 0.08277465283381506


################################################################################
#                                 End of File                                  #
################################################################################

