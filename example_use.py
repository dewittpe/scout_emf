################################################################################
#
# purpose: using the refactored functions defined in import_ecm_results.py
# compare DeWitt's refactored results to the results of the original work done
# via the EMF_Scout.py script.
#
################################################################################
import json
import pandas as pd
import re
import datetime
import numpy as np
from collections import defaultdict
from scout_emf_methods import isfloat
from scout_emf_methods import import_ecm_results

################################################################################
ecms, ecm_mas, finanical_metrics, filter_variables, on_site_generation = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
ecm_mas.groupby(["end_use", "fuel_type"]).count()

on_site_generation.info()
on_site_generation

filter_variables.info()
filter_variables

finanical_metrics.info()
finanical_metrics

ecm_mas.info()
ecm_mas

all(on_site_generation.value.apply(isfloat))
all(on_site_generation.year.str.contains(r"^\d{4}$"))


ecms, ecm_mas, finanical_metrics, filter_variables, on_site_generation = import_ecm_results("./Results_Files_3/ecm_results_2.json")
ecm_mas.groupby(["end_use", "fuel_type"]).count()

ecms, ecm_mas, finanical_metrics, filter_variables, on_site_generation = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")
ecm_mas.groupby(["end_use", "fuel_type"]).count()


ecms

ecm_mas.value = ecm_mas.value.apply(float)
ecm_mas.value = ecm_mas.value.apply(float)
ecm_mas.info()

set(ecm_mas.year)

ecm_mas

finanical_metrics

filter_variables
on_site_generation

[itm[0] for itm in ecm_mas.fuel_type.str.findall("^\d{4}$") if len(itm) > 0]

[ i for i in range(len(ecm_mas)) if ecm_mas.fuel_type[i].str.contains("^\d{4}$") ]

ecm_mas[ecm_mas.fuel_type.str.contains("^\d{4}$")]

set(ecm_mas.electric)

ecm_mas.groupby(["end_use", "electric"]).count()


x = ecm_mas[ecm_mas.electric.isna()]\
        .groupby(["ecm", "scenario", "metric", "region", "building_class", "end_use", "year"])\
        .agg({"value" : "sum"})

y = ecm_mas[ecm_mas.electric.notna()]\
        .groupby(["ecm", "scenario", "metric", "region", "building_class", "end_use", "year"])\
        .agg({"value" : "sum"})

x.reset_index(inplace = True)
y.reset_index(inplace = True)

len(x)
len(y)

z = pd.merge(x, y, how = "outer", on = ["ecm", "scenario", "metric", "region", "building_class", "end_use", "year"])

z[
        (z.scenario == "Max adoption potential") &
        (z.metric == "Avoided CO\u2082 Emissions (MMTons)") &
        (z.region == "AIA CZ1") &
        (z.building_class == "Commercial (Existing)") & 
        #(z.end_use == "Lighting") &
        (z.ecm == "Prospective Com. Comfort Ctl. 2030")
        ]


set(
x[
        (x.scenario == "Max adoption potential") &
        (x.metric == "Avoided CO\u2082 Emissions (MMTons)") &
        (x.region == "AIA CZ1") &
        (x.building_class == "Commercial (Existing)") & 
        #(x.end_use == "Lighting") &
        (x.ecm == "Prospective Com. Comfort Ctl. 2030")
        ].end_use
)

set(
y[
        #(y.scenario == "Max adoption potential") &
        #(y.metric == "Avoided CO\u2082 Emissions (MMTons)") &
        #(y.region == "AIA CZ1") &
        #(y.building_class == "Commercial (Existing)") & 
        #(y.end_use == "Lighting") &
        (y.ecm == "Prospective Com. Comfort Ctl. 2030")
        ].end_use
)

[ i for i in set(y.ecm) if i in set(x.ecm)]
[ i for i in set(x.ecm) if i in set(y.ecm)]



set(ecm_mas.electric)


filter_variables

finanical_metrics_1

set(ecms.lvl1)








################################################################################
#                                  SECTION 1                                   #
#                                                                              #
#          Import and Compare aggregation of ecm_results*.json files           #
#                                                                              #
################################################################################
# Import the example result files
ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
ecm_2 = import_ecm_results("./Results_Files_3/ecm_results_2.json")
ecm_3 = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")

baseline_energy = import_baseline_energy_data("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")
baseline_building = import_baseline_building_data("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")

baseline_building

ecm_1
ecm_2
ecm_3.info()
baseline_energy.info()
baseline_energy

ecm_1.info()
emf_mapping_base_string(ecm_1.variable)

range(len(ecm_1.variable))

set(ecm_1["fuel_type"])
set(ecm_2["fuel_type"]) 
set(ecm_3["fuel_type"])
set(baseline_energy["fuel"])

# aggregate the results
emf_1 = aggregate_ecm_results(ecm_1)
emf_2 = aggregate_ecm_results(ecm_2)
emf_3 = aggregate_ecm_results(ecm_3)

################################################################################
# import the original results
emf_1_orig = pd.read_csv("EMF_Scout_output/ecm_results_1-1.csv")
emf_2_orig = pd.read_csv("EMF_Scout_output/ecm_results_2.csv")
emf_3_orig = pd.read_csv("EMF_Scout_output/ecm_results_3-1.csv")

emf_1_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)
emf_2_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)
emf_3_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)

################################################################################
# compare the refactored work against the original work
emf_1 = emf_1[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]
emf_2 = emf_2[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]
emf_3 = emf_3[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]

# compare refactor approach to original
emf_1 = emf_1.merge(emf_1_orig, on = ["emf_string"], how = "outer",
        suffixes = ("_refactor", "_orig"))
emf_2 = emf_2.merge(emf_2_orig, on = ["emf_string"], how = "outer",
        suffixes = ('_refactor', "_orig"))
emf_3 = emf_3.merge(emf_3_orig, on = ["emf_string"], how = "outer",
        suffixes = ('_refactor', "_orig"))

emf_1["match"] = \
        (abs(emf_1["2025_refactor"] - emf_1["2025_orig"]) < 1e-8) &\
        (abs(emf_1["2030_refactor"] - emf_1["2030_orig"]) < 1e-8) &\
        (abs(emf_1["2035_refactor"] - emf_1["2035_orig"]) < 1e-8) &\
        (abs(emf_1["2040_refactor"] - emf_1["2040_orig"]) < 1e-8) &\
        (abs(emf_1["2045_refactor"] - emf_1["2045_orig"]) < 1e-8) &\
        (abs(emf_1["2050_refactor"] - emf_1["2050_orig"]) < 1e-8)

emf_2["match"] = \
        (abs(emf_2["2025_refactor"] - emf_2["2025_orig"]) < 1e-8) &\
        (abs(emf_2["2030_refactor"] - emf_2["2030_orig"]) < 1e-8) &\
        (abs(emf_2["2035_refactor"] - emf_2["2035_orig"]) < 1e-8) &\
        (abs(emf_2["2040_refactor"] - emf_2["2040_orig"]) < 1e-8) &\
        (abs(emf_2["2045_refactor"] - emf_2["2045_orig"]) < 1e-8) &\
        (abs(emf_2["2050_refactor"] - emf_2["2050_orig"]) < 1e-8)

emf_3["match"] = \
        (abs(emf_3["2025_refactor"] - emf_3["2025_orig"]) < 1e-8) &\
        (abs(emf_3["2030_refactor"] - emf_3["2030_orig"]) < 1e-8) &\
        (abs(emf_3["2035_refactor"] - emf_3["2035_orig"]) < 1e-8) &\
        (abs(emf_3["2040_refactor"] - emf_3["2040_orig"]) < 1e-8) &\
        (abs(emf_3["2045_refactor"] - emf_3["2045_orig"]) < 1e-8) &\
        (abs(emf_3["2050_refactor"] - emf_3["2050_orig"]) < 1e-8)

################################################################################
# View the matching and non-matching rows

###
### EMF 1
###

# matching rows
emf_1[emf_1.match]

# missmatched rows
emf_1[~emf_1.match]

# in both refactor and original work but numerially different
emf_1[~emf_1.match & emf_1["2025_refactor"].notna() & emf_1["2025_orig"].notna()]

# in the refactor but not in the original work
emf_1[~emf_1.match & emf_1["2025_refactor"].notna() & emf_1["2025_orig"].isna()]

# in the original work, but not in the refactor
emf_1[~emf_1.match & emf_1["2025_refactor"].isna() & emf_1["2025_orig"].notna()]

###
### EMF 2
###

# matching rows
emf_2[emf_2.match]

# missmatched rows
emf_2[~emf_2.match]

# in both refactor and original work but numerially different
emf_2[~emf_2.match & emf_2["2025_refactor"].notna() & emf_2["2025_orig"].notna()]

# in the refactor but not in the original work
emf_2[~emf_2.match & emf_2["2025_refactor"].notna() & emf_2["2025_orig"].isna()]

# in the original work, but not in the refactor
emf_2[~emf_2.match & emf_2["2025_refactor"].isna() & emf_2["2025_orig"].notna()]

###
### EMF 3
###

# matching rows
emf_3[emf_3.match]

# missmatched rows
emf_3[~emf_3.match]

# in both refactor and original work but numerially different
emf_3[~emf_3.match & emf_3["2025_refactor"].notna() & emf_3["2025_orig"].notna()]

# in the refactor but not in the original work
emf_3[~emf_3.match & emf_3["2025_refactor"].notna() & emf_3["2025_orig"].isna()]

# in the original work, but not in the refactor
emf_3[~emf_3.match & emf_3["2025_refactor"].isna() & emf_3["2025_orig"].notna()]

################################################################################
# ECM 1 Explore

# example issue -- values are reported in the original work not in the refactor
# In this case the original work reports a zero but the combination of
# building_class == Commercial, end_use == Other, and fuel_type = Oil is not in
# raw data.
emf_1[emf_1.emf_string == "BASN*Final Energy|Buildings|Commercial|Other|Oil"]

# not in the raw data the only end use is "Heating"
set(
    ecm_1[(ecm_1.variable == "Energy Savings (MMBtu)") &
            (ecm_1.region == "BASN") &
            (ecm_1.building_class == "Commercial") &
            (ecm_1.fuel_type2 == "Oil")
            ].end_use
)

# are all of the values zero?  -- This suggests that these were asked for and
# set to zero when nothing was found in the raw data.
all(emf_1[~emf_1.match & emf_1["2025_refactor"].isna() & emf_1["2025_orig"].notna()]["2025_orig"] == 0.0)
all(emf_1[~emf_1.match & emf_1["2030_refactor"].isna() & emf_1["2030_orig"].notna()]["2030_orig"] == 0.0)
all(emf_1[~emf_1.match & emf_1["2035_refactor"].isna() & emf_1["2035_orig"].notna()]["2035_orig"] == 0.0)
all(emf_1[~emf_1.match & emf_1["2040_refactor"].isna() & emf_1["2040_orig"].notna()]["2040_orig"] == 0.0)
all(emf_1[~emf_1.match & emf_1["2045_refactor"].isna() & emf_1["2045_orig"].notna()]["2045_orig"] == 0.0)
all(emf_1[~emf_1.match & emf_1["2050_refactor"].isna() & emf_1["2050_orig"].notna()]["2050_orig"] == 0.0)

# Some of the aggregations found in the refactor that are not in the original
# work are arregations of
#   emf_string, fuel_type2
#   emf_string, building_class, end_use2
# The non-zero values, and just the presence of these rows indicate that
# suggest they were overlooked in the original work.  Further, the rows are
# aggregated into higher levels which would account for the numeric differences
# between the refactor and the original work.
emf_1[~emf_1.match & emf_1["2025_refactor"].notna() & emf_1["2025_orig"].isna()]

# Per request - by EMF string report the matches/missmatches by Region
emf_1.loc[emf_1.match, "refactor_vs_original"] = "refactor == original"
emf_1.loc[~emf_1.match & emf_1["2025_refactor"].notna() & emf_1["2025_orig"].notna(), "refactor_vs_original"] = "refactor != original"
emf_1.loc[~emf_1.match & emf_1["2025_refactor"].isna() & emf_1["2025_orig"].notna(), "refactor_vs_original"] = "not in refactor; in original"
emf_1.loc[~emf_1.match & emf_1["2025_refactor"].notna() & emf_1["2025_orig"].isna(), "refactor_vs_original"] = "in refactor; not in original"

emf_1["ecm"] = emf_1.emf_string.str.split("*", expand = True)[0]
emf_1["emf_string2"] = emf_1.emf_string.str.split("*", expand = True)[1]

# save a csv and then create a useful xlsx
emf_1.pivot(index = "emf_string2",
        columns = "ecm",
        values = "refactor_vs_original")\
     .to_csv('refactor_vs_original.csv')


################################################################################
# ECM 2 Explore

emf_2[~emf_2.match & emf_2["2025_refactor"].isna() & emf_2["2025_orig"].notna()]

# WTF?  Okay, so in the original work there is a row for
emf_2[emf_2.emf_string.str.contains("BASN*Final Energy|Buildings|Residential|Other", regex = False) &
        (emf_2["2025_orig"] > 0)
        ]
emf_2[emf_2.emf_string.str.contains("BASN*Final Energy|Buildings|Residential|Other", regex = False) &
        (emf_2["2025_orig"] > 0)
        ].emf_string.tolist()

# but the raw data has no fuel type
ecm_2[(ecm_2.emf_string == "BASN*Final Energy|Buildings") &
        (ecm_2.building_class == "Residential") &
        (ecm_2.end_use2 == "Other")
        ].fuel_type

# The non-zero values in the original work suggest there should be data in the
# raw json, but that does not seem to be the case.


################################################################################
#                                  SECTION 2                                   #
#                                                                              #
#                  Import, convert, and compare Baseline Data                  #
#                                                                              #
################################################################################
# Import baseline data
baseline_energy   = import_baseline_energy_data("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")
baseline_energy

baseline_building = import_baseline_building_data("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")

# covert coeff
convert_coeffs = import_conversion_coeffs( './supporting_data/convert_data/emm_region_emissions_prices.json')

# fresh read of aggregated ecm results
ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
emf_1 = aggregate_ecm_results(ecm_1)


baseline_energy
ecm_1


# covert energy to co2
ecm_1.info()

set(ecm_1.fuel_type)
set(ecm_1.fuel_type2)
ecm_1
emf_1

convert_coeffs.info()
convert_coeffs[["concept", "units", "region", "year", "value"]]

convert_coeffs.loc[convert_coeffs.concept == "CO2 intensity of electricity",
        ["concept", "units", "region", "year", "value"]
        ]

convert_coeffs[["concept", "units", "region", "year", "value"]]

convert_energy_to_co2(convert_coeffs)

################################################################################
time_delta = datetime.datetime.now() - tic0
print("\n\nTiming:")
print(f"example_use.py completed in: {time_delta}")

################################################################################
#                                 End of File                                  #
################################################################################

