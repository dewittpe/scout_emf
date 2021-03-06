################################################################################
# Example use, with timing, for scout package
################################################################################
import scout
import json
import pandas as pd
import re
import datetime
import numpy as np

class Timer:
    def __init__(self, name = None):
        self.name = name
    
    def __enter__(self):
        self.tic = datetime.datetime.now()

    def __exit__(self, type, value, traceback):
        if self.name:
            print('[%s]' % self.name,)
        print('Elapsed: %s' % (datetime.datetime.now() - self.tic))

################################################################################
# ECM Results
#
# Can provide path to a .json file _or_ a .gz file containing the needed json.
# Performance difference is negligable.
with Timer(name = "Import ecm_results_1-1.json"):
    results_1 = scout.ecm_results(path = "./Results_Files_3/ecm_results_1-1.json.gz")

with Timer(name = "Import ecm_results_2.json"):
    results_2 = scout.ecm_results(path = "./Results_Files_3/ecm_results_2.json.gz")

with Timer(name = "Import ecm_results_3-1.json"):
    results_3 = scout.ecm_results(path = "./Results_Files_3/ecm_results_3-1.json.gz")

# An info method is provided
results_1.info()

# The by_category_vs_overall returns a dict of DataFrames for where the
# aggregated "By Category" values differs from the "Overall" by more than a
# given tol(erance), the default is tol = 1e-8
with Timer("compare aggrgated 'By Category' to 'Overall' values"):
    results_1.by_category_vs_overall()
    results_2.by_category_vs_overall()
    results_3.by_category_vs_overall()


d1 = results_1.by_category_aggreation_vs_overall
d2 = results_2.by_category_aggreation_vs_overall
d3 = results_3.by_category_aggreation_vs_overall

print("For results_1")
print("  - Markets and Savings")
print(d1["Markets and Savings"])
print("\n\n  - On-site Generation")
print(d1["On-site Generation"])

print("For results_2")
print("  - Markets and Savings")
print(d2["Markets and Savings"])
print(f"min delta: {min(d2['Markets and Savings'].delta)}")
print(f"max delta: {max(d2['Markets and Savings'].delta)}")
print("\n\n  - On-site Generation")
print(d2["On-site Generation"])
print(f"min delta: {min(d2['On-site Generation'].delta)}")
print(f"max delta: {max(d2['On-site Generation'].delta)}")

print("For results_3")
print("  - Markets and Savings")
print(d3["Markets and Savings"])
print("\n\n  - On-site Generation")
print(d3["On-site Generation"])

################################################################################
# Aggregate ECM Results to EMF summaries
assert results_1.emf_aggregation is None
assert results_2.emf_aggregation is None
assert results_3.emf_aggregation is None

with Timer(name = "aggregate results_1 for emf"):
    results_1.aggregate_for_emf()

with Timer(name = "aggregate results_2 for emf"):
    results_2.aggregate_for_emf()

with Timer(name = "aggregate results_3 for emf"):
    results_3.aggregate_for_emf()


assert isinstance(results_1.emf_aggregation, pd.DataFrame)
assert isinstance(results_2.emf_aggregation, pd.DataFrame)
assert isinstance(results_3.emf_aggregation, pd.DataFrame)

print(results_1.emf_aggregation)
print(results_2.emf_aggregation)
print(results_3.emf_aggregation)


################################################################################
from scout import import_baseline
from scout.utilities import json_to_df

bldg_metadata, baseline =\
        import_baseline("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")


bldg_metadata
baseline.info()
baseline

# emf_aggregation of ecm_results
results_1.aggregate_for_emf()
results_2.aggregate_for_emf()
results_3.aggregate_for_emf()

# view aggregations
results_1.emf_aggregation
results_2.emf_aggregation
results_3.emf_aggregation



################################################################################
# Aggregate ECM Results to EMF summaries
ecm_mas_1_modified, emf_1 = ecm_results_to_emf_aggregation(ecm_mas_1)
ecm_mas_2_modified, emf_2 = ecm_results_to_emf_aggregation(ecm_mas_2)
ecm_mas_3_modified, emf_3 = ecm_results_to_emf_aggregation(ecm_mas_3)

print(emf_1)
print(emf_2)
print(emf_3)


################################################################################
#                                  SECTION 1                                   #
#                                                                              #
#          Import and Compare aggregation of ecm_results*.json files           #
#                                                                              #
################################################################################

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
baseline

# emf_fuel_type
baseline["emf_fuel_type"] = np.nan

baseline.loc[baseline.fuel_type == "natural gas", "emf_fuel_type"] = "Gas"

baseline.loc[
        (baseline.fuel_type == "natural gas") &
        (baseline.technology_type.str.contains("LPG")), "emf_fuel_type"] = "Gas_lpg"


set(baseline[baseline.fuel_type == "electricity"].end_use)

set(
baseline[(baseline.technology_type.notna()) &
        (baseline.technology_type.str.contains("kerosene"))
        ].fuel_type)

baseline[baseline.technology_type.isna()]


set(baseline.fuel_type)
set(baseline.end_use)
set(baseline.demand_supply)
set(baseline.technology_type)  #  THIS MIGHT NEED TO BE
set(baseline.stock_energy)

baseline[
        (baseline.fuel_type == "natural gas") &
        (baseline.end_use   == "heating")
        ]

set(
baseline[
        baseline.technology_type == "secondary heater (coal)"
        ].fuel_type
)

set(
baseline[
        (baseline.fuel_type == "other fuel")
        ].technology_type
)


################################################################################
time_delta = datetime.datetime.now() - tic0
print("\n\nTiming:")
print(f"example_use.py completed in: {time_delta}")

################################################################################
#                                 End of File                                  #
################################################################################

