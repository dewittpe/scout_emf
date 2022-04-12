import json
import pandas as pd
import re
import time
from import_ecm_results import import_ecm_results
from import_ecm_results import import_baseline_fuel_data
from import_ecm_results import import_baseline_non_fuel_data
from import_ecm_results import aggregate_emf

fuel_b     = import_baseline_fuel_data("./mseg_res_com_emm.json")

non_fuel_b = import_baseline_non_fuel_data("./mseg_res_com_emm.json")


df = pd.DataFrame.from_dict(fuel_b)

df[df["year"].notnull()]


fuel_b[fuel_b["year"] == 2035]
all(fuel_b['year'] == "2050")

non_fuel_b


df = pd.DataFrame.from_dict(b)
df
df[df["value"].isna()]

df["leaf"].is()

[v for v in df["leaf"]]



[i for i in range(len(df)) if df[i]["leaf"] is None]
[df[i]["leaf"] for i in range(len(df))]


# Import the example result files
ecm_1 = import_ecm_results("./Results_Files_3/ecm_results_1-1.json")
ecm_2 = import_ecm_results("./Results_Files_3/ecm_results_2.json")
ecm_3 = import_ecm_results("./Results_Files_3/ecm_results_3-1.json")
ecm_4 = import_ecm_results("ecm_results_4.json")



for i in range(len(b)):
    print(list(b[i]["leaf"]))


# fuels
["electricity", "natural gas", "distillate", "other fuel"]

baseline = json.load(open("./mseg_res_com_emm_NEW.json", "r"))
list(baseline)

list(baseline["TRE"])
list(baseline["TRE"]["single family home"])
list(baseline["TRE"]["lodging"])
list(baseline["TRE"]["food service"])

list(baseline["TRE"]["single family home"]['total homes'])
list(baseline["TRE"]["single family home"]['new homes'])
list(baseline["TRE"]["single family home"]['total square footage'])




list(baseline["TRE"]["single family home"]['electricity'])
list(baseline["TRE"]["single family home"]['electricity']['heating'])
list(baseline["TRE"]["single family home"]['electricity']['heating']['demand'])
list(baseline["TRE"]["single family home"]['electricity']['heating']['demand']['wall'])
baseline["TRE"]["single family home"]['electricity']['heating']['demand']['wall']['stock']
baseline["TRE"]["single family home"]['electricity']['heating']['demand']['wall']['energy']
baseline["TRE"]["single family home"]['electricity']['heating']['demand']['wall']['energy']['2018']



for ecm in list(baseline):
    print("\n\nECM: " + ecm)
    for bd in list(baseline[ecm]): 
        print("\nBuilding: " + bd)
        print(list(baseline[ecm][bd]))



# aggregate the results
emf_1 = aggregate_emf(ecm_1)
emf_2 = aggregate_emf(ecm_2)
emf_3 = aggregate_emf(ecm_3)
emf_4 = aggregate_emf(ecm_4)

# import the original results
emf_1_orig = pd.read_csv("ecm_results_1-1.csv")
emf_2_orig = pd.read_csv("ecm_results_2.csv")
emf_3_orig = pd.read_csv("ecm_results_3-1.csv")

emf_1_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)
emf_2_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)
emf_3_orig.rename(columns = {"Unnamed: 0" : "emf_string"}, inplace = True)

# compare the refactored work against the original work
emf_1 = emf_1[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]
emf_2 = emf_2[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]
emf_3 = emf_3[["emf_string", "2025", "2030", "2035", "2040", "2045", "2050"]]

# compare my approach to original
emf_1 = emf_1.merge(emf_1_orig, on = ["emf_string"], how = "outer", suffixes = ("_refactor", "_orig"))
emf_2 = emf_2.merge(emf_2_orig, on = ["emf_string"], how = "outer", suffixes = ('_refactor', "_orig"))
emf_3 = emf_3.merge(emf_3_orig, on = ["emf_string"], how = "outer", suffixes = ('_refactor', "_orig"))

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

### EMF 1 ###

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

### EMF 2 ###

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


### EMF 3 ###

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
emf_1.pivot(index = "emf_string2", columns = "ecm", values = "refactor_vs_original").to_csv('refactor_vs_original.csv')


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
#                                 End of File                                  #
################################################################################

