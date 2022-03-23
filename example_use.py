import json
import pandas as pd
import re
import time
from import_ecm_results import import_ecm_results

ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
#ecm_2 = import_ecm_results("./Results_Files_3/ecm_results_2.json")
#ecm_3 = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")
#ecm_4 = import_ecm_results("ecm_results_4.json")




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


# original work
d = pd.read_csv("ecm_results_1-1.csv")
d.info()
d.rename(columns = {"Unnamed: 0" :  "emf_string"}, inplace = True)

# compare my approach to original
a = a[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]

b = a.merge(d, on = ["emf_string"], how = "outer")
b["match"] = \
        (abs(b["2025_x"] - b["2025_y"]) < 1e-8) &\
        (abs(b["2030_x"] - b["2030_y"]) < 1e-8) &\
        (abs(b["2035_x"] - b["2035_y"]) < 1e-8) &\
        (abs(b["2040_x"] - b["2040_y"]) < 1e-8) &\
        (abs(b["2045_x"] - b["2045_y"]) < 1e-8) &\
        (abs(b["2050_x"] - b["2050_y"]) < 1e-8)

# matching rows
b[b.match]

# non-matching rows
b[~b.match]

# it appears that there are aggregation "errors",
# rows missing in the refactor work which exist in the original work and visa
# versa
#
# FOR EXAMPLE: There is no rows in the following.  In the original work there would be
# output for this combination and the value set to 0.  In the current version of
# what @dewittpe has built this row is omitted from the output becuase there is
# no information to start with.
ecm_1[(ecm_1.region == "BASN") & (ecm_1.building_class == "Commercial") & (ecm_1.end_use2 == "Other") & (ecm_1.fuel_type2 == "Oil")]

################################################################################
#                                 End of File                                  #
################################################################################

