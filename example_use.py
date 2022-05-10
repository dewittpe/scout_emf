# author: Peter DeWitt
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
from scout_emf_methods import import_ecm_results
from scout_emf_methods import import_baseline_energy_data
from scout_emf_methods import import_baseline_energy_data2
from scout_emf_methods import import_baseline_building_data
from scout_emf_methods import aggregate_ecm_results
from scout_emf_methods import import_conversion_coeffs
from scout_emf_methods import convert_energy_to_co2
from scout_emf_methods import mapping_emf_base_string
from scout_emf_methods import mapping_building_class
from scout_emf_methods import mapping_direct_fuel
from scout_emf_methods import mapping_end_uses


f = open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm", "r")
baseline = json.load(f)
f.close()

def depth(x):
    if isinstance(x, dict) and x:
        return 1 + max(depth(x[a]) for a in x)
    elif isinstance(x, list) and x:
        return 1 + max(depth(a) for a in x)
    return 0

depth(baseline)

x = {"lvl0" : [], "lvl1" : []}


dict(zip(list(baseline), list(baseline)))


baseline.keys()

pd.DataFrame.from_dict(baseline)













def unique(list1):
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)

    for x in unique_list:
        print(x)

def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)


def id_generator(dict_var, leaf):
    for k, v in dict_var.items():
        if k == leaf:
            yield v
        elif isinstance(v, dict):
            for id_val in id_generator(v, leaf):
                yield id_val

# baseline_energy1 = import_baseline_energy_data("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")
# about 2.2 seconds
baseline_energy2 = import_baseline_energy_data2("./supporting_data/stock_energy_tech_data/mseg_res_com_emm")
pd.DataFrame.from_dict(baseline_energy2)




f = open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm", "r")
baseline = json.load(f)
f.close()

pd

list(baseline)

id_generator(baseline, "2016")

for _ in id_generator(baseline, "2024"):
    print(_)

isinstance(baseline, dict)
isinstance(baseline["TRE"], dict)
isinstance(baseline["TRE"]["single family home"], dict)
isinstance(baseline["TRE"]["single family home"]["electricity"], dict)
isinstance(baseline["TRE"]["single family home"]["electricity"]["TVs"], dict)
isinstance(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"], dict)
isinstance(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"], dict)
isinstance(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"]["2015"], dict)

def walker(x):
    if isinstance(x, dict):
        for l in list(x):
            if not isinstance(x[l], dict):
                yield {l:x[l]}
            else:
                yield from walker(x[l])

for _ in walker(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"]["2015"]):
    print(_)

for _ in walker(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"]):
    print(_)

for _ in walker(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]):
    print(_)


def walker(x, ks = None):
    if ks is None:
        ks = []
    for k,v in x.items():
        if not isinstance(v, dict):
            ks.append(v)
        else:
            ks.append(k)
            walker(x[k], ks)
    return ks

x = walker(baseline)
len(x)

x[11]


baseline["TRE"]["single family home"]["total homes"]


for k,v in baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"].items():
    print(k, v)
    print(isinstance(v, dict))

for k,v in baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"].items():
    print(k, v)
    print(isinstance(v, dict))


list(baseline["TRE"]["single family home"]["electricity"])
list(baseline["TRE"]["single family home"]["electricity"]["TVs"])
list(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"])
list(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"])
list(baseline["TRE"]["single family home"]["electricity"]["TVs"]["TV"]["stock"]["2015"])

###
tic = datetime.datetime.now()

bldg_vars = ["total homes", "new homes" , "total square footage", "new square footage"]

f = open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm", "r")
baseline = json.load(f)
f.close()

fuels = [{"region" : region, "bldg" : bd, "fuel_type": ft, "end_use": eu, "leaf" : l}\
        for region in list(baseline)\
        for bd  in list(baseline[region])\
        for ft  in list(baseline[region][bd]) if ft not in bldg_vars
        for eu  in list(baseline[region][bd][ft])
        for l   in     [baseline[region][bd][ft][eu]]
        ]

# "flatten" the list of dictionaries to _a_ dictionaries with array entries
res1 = defaultdict(list)
{res1[key].append(sub[key]) for sub in fuels for key in sub}

# Next, the leaf can have one of three general concepts for keys:
# 1. stock/energy
# 2. demand/supply
# 3. appliances (including lightbulbs)
# 
# res2 expands from res1 to have three additional concepts and drill down one
# level on the leaf.

res2 = defaultdict(list)
for i in range(len(res1["leaf"])):
    for leaf in list(res1["leaf"][i]):
        res2["region"].append(res1["region"][i])
        res2["bldg"].append(res1["bldg"][i])
        res2["fuel_type"].append(res1["fuel_type"][i])
        res2["end_use"].append(res1["end_use"][i])
        res2["leaf"].append(res1["leaf"][i][leaf])
        if leaf in ["stock", "energy"]:
            res2["stock_energy"].append(leaf)
            res2["demand_supply"].append(np.nan)
            res2["appliance"].append(np.nan)
        elif leaf in ["demand", "supply"]:
            res2["stock_energy"].append(np.nan)
            res2["demand_supply"].append(leaf)
            res2["appliance"].append(np.nan)
        else:
            res2["stock_energy"].append(np.nan)
            res2["demand_supply"].append(np.nan)
            res2["appliance"].append(leaf)

# Next, the leafs could be one of three sets:
# 1. year
# 2. stock/energy
# 3. appliance
regex = re.compile(r"\d{4}")
res3 = defaultdict(list)

for i in range(len(res2["leaf"])):
    for leaf in list(res2["leaf"][i]):
        res3["region"].append(res2["region"][i])
        res3["bldg"].append(res2["bldg"][i])
        res3["fuel_type"].append(res2["fuel_type"][i])
        res3["end_use"].append(res2["end_use"][i])
        res3["demand_supply"].append(res2["demand_supply"][i])
        if leaf in ["N", "A"]:
            res3["stock_energy"].append(res2["stock_energy"][i])
            res3["year"].append(np.nan)
            res3["appliance"].append(res2["appliance"][i])
            res3["leaf"].append(np.nan)
        elif leaf in ["stock", "energy"]:
            res3["stock_energy"].append(leaf)
            res3["year"].append(np.nan)
            res3["appliance"].append(res2["appliance"][i])
            res3["leaf"].append(res2["leaf"][i][leaf])
        elif regex.search(leaf):
            res3["stock_energy"].append(res2["stock_energy"][i])
            res3["year"].append(leaf)
            res3["appliance"].append(res2["appliance"][i])
            res3["leaf"].append(res2["leaf"][i][leaf])
        else:
            res3["stock_energy"].append(res2["stock_energy"][i])
            res3["year"].append(np.nan)
            res3["appliance"].append(leaf)
            res3["leaf"].append(res2["leaf"][i][leaf])

# Now, if the leaf is not None, then it could be year or energy/stock

temp = defaultdict(list)
res4 = defaultdict(list)
for i in range(len(res3["leaf"])):
    if res3["leaf"][i] is np.nan or isfloat(res3["leaf"][i]) or res3["leaf"][i] == {}:
        for k in list(res3):
            res4[k].append(res3[k][i])
            res4["value"].append(res3["leaf"][i])
            res4["leaf"].append(np.nan)
    else:
        for k in [k for k in list(res3) if k not in ["stock_energy", "year", "leaf", "value"]]:
            res4[k].append(res3[k][i])
        for leaf in list(res3["leaf"][i]):
            if leaf in ["N", "A"]:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(np.nan)
                res4["leaf"].append(np.nan)
                res4["value"].append(np.nan)
            elif leaf in ["stock", "energy"]:
                res4["stock_energy"].append(leaf)
                res4["year"].append(np.nan)
                res4['value'].append(np.nan)
                res4["leaf"].append(res3["leaf"][i][leaf])
            elif regex.search(leaf):
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(leaf)
                res4['value'].append(np.nan)
                res4["leaf"].append(res3["leaf"][i][leaf])
            else:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(np.nan)
                res4["appliance"].append(leaf)
                res4["leaf"].append(res3["leaf"][i][leaf])





pd.DataFrame.from_dict(res4)

for k in list(res4):
    print(k + ": " + str(res4[k][149264]))

for k in list(res4):
    print(k + ": " + str(len(res4[k])))



for k in list(res3):
    print(k + ": " + str(res3[k][149264]))

res3["leaf"][149264] == {}

temp = defaultdict(list)
for i in range(len(res4["leaf"])):
    print("i: " + str(i))
    print(res4["leaf"][i])
    temp["keys"].append(list(res4["leaf"][i]))

unique(temp["keys"])

list(res4)
for k in list(res4):
    print(k + ": " + str(len(res4[k])))



    for leaf in list(res3["leaf"][i]):
        if leaf is np.nan:
            for k in list(res3):
                res4[k].append(res3[k][i])
        else:
            for k in [k for k in list(res3) if k not in ["stock_energy", "year", "leaf"]]:
                res4[k].append(res3[k][i])

            if leaf in ["N", "A"]:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(res3["year"][i])
                res4["leaf"].append(np.nan)
            elif leaf in ["stock", "energy"]:
                res4["stock_energy"].append(leaf)
                res4["year"].append(res3["year"][i])
                res4["leaf"].append(res3["leaf"][i][leaf])
            else:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(leaf)
                res4["leaf"].append(res3["leaf"][i][leaf])

if verbose:
    time_delta = datetime.datetime.now() - tic
    print(f"{path} imported and coerced to a DataFrame in {time_delta}")
return(res4)

    # finally, one more run though to get the yearly data
    fuels_5 = []

    for i in range(len(fuels_4)):
        d1 = {    "region"    : fuels_4[i]["region"]
                , "bldg"      : fuels_4[i]["bldg"]
                , "fuel"      : fuels_4[i]["fuel"]
                , "enduse"    : fuels_4[i]["enduse"]
                , "se"        : fuels_4[i]["se"]
                , "ds"        : fuels_4[i]["ds"]
                , "appliance" : fuels_4[i]["appliance"]
                , "year"      : fuels_4[i]["year"]
                , "leaf"      : fuels_4[i]["leaf"]
                , "value"     : fuels_4[i]["value"]
                }
        if fuels_4[i]["leaf"] is not None:
            for leaf in list(fuels_4[i]["leaf"]):
                if leaf in ["N", "A"]:
                    d1["leaf"] = None
                else:
                    d1["year"] = leaf
                    d1["value"] = fuels_4[i]["leaf"][leaf]
                    d1["leaf"] = None
        fuels_5.append(d1)

    rtn = pd.DataFrame.from_dict(fuels_5)
    rtn.drop(axis = 1, inplace = True, columns = "leaf")

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a DataFrame in {time_delta}")

    return rtn

# }}}

##########################################################################################

res3 = baseline_energy2
len(res3)
len(res3["leaf"])

for i in range(len(res3['leaf'])):
    print("i: " + str(i))
    print( list(res3["leaf"][i]) )

res3["leaf"][32]

list(res3)

len(res3['year'])
len(res3['leaf'])

res3['year'][32]


res4 = defaultdict(list)
for i in range(len(res3["leaf"])):
    print(i)

    if res3["leaf"][i] is np.nan or isfloat(res3["leaf"][i]):


    for leaf in list(res3["leaf"][i]):
        if leaf is np.nan or isfloat(leaf):
            for k in list(res3):
                res4[k].append(res3[k][i])
                res4[value].append(leaf)
        else:
            for k in [k for k in list(res3) if k not in ["stock_energy", "year", "leaf"]]:
                res4[k].append(res3[k][i])
            if leaf in ["N", "A"]:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(res3["year"][i])
                res4["leaf"].append(np.nan)
            elif leaf in ["stock", "energy"]:
                res4["stock_energy"].append(leaf)
                res4["year"].append(res3["year"][i])
                res4["leaf"].append(res3["leaf"][i][leaf])
            else:
                res4["stock_energy"].append(res3["stock_energy"][i])
                res4["year"].append(leaf)
                res4["leaf"].append(res3["leaf"][i][leaf])

leaf



















regex = re.compile(r"\d{4}")
res4 = defaultdict(list)
res4["value"] = []

for i in range(len(res3["leaf"])):
    l = res3["leaf"][i]
    if l is np.nan:
        for k in [k for k in list(res3)]:
            res4[k].append(res3[k][i])
        res4["value"].append(np.nan)
    elif isinstance(l, float): 
        for k in [k for k in list(res3)]:
            res4[k].append(res3[k][i])
        res4["value"].append(l)
    else:
        for leaf in list(res3["leaf"][i]):
            for k in [k for k in list(res3) if k not in ["leaf", "stock_energy", "year"]]:
                res4[k].append(res3[k][i])
            if leaf in ["N", "A"]:
                res4["leaf"].append(np.nan)
                res4["stock_energy"].append(np.nan)
                res4["year"].append(np.nan)
                res4["value"].append(np.nan)
            elif leaf in ["stock", "energy"]:
                res4["leaf"].append(res3["leaf"][i][leaf])
                res4["stock_energy"].append(leaf)
                res4["year"].append(np.nan)
                res4["value"].append(np.nan)
            elif regex.search(leaf):
                res4["leaf"].append(res3["leaf"][i][leaf])
                res4["stock_energy"].append(np.nan)
                res4["year"].append(leaf)
                res4["value"].append(np.nan)
            else:
                pass


        print(f"i = {i}; l = {l}")

pd.DataFrame.from_dict(res4)

list(res4)



baseline_energy2["leaf"][1].keys()
baseline_energy2["leaf"][101] is float

isfloat(baseline_energy2["leaf"][101])

isinstance(baseline_energy2["leaf"][101], float)


def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False




baseline_energy2["leaf"][157422] is np.nan

pd.DataFrame.from_dict(baseline_energy2)[["leaf",
    "stock_energy", "demand_supply", "appliance", "year"]]

things = ["a", "b", "c", "d", "e"]


[k for k in things if k not in ["c", "e"]]
    print(k)




mapping_emf_base_string()
mapping_building_class()
mapping_direct_fuel()
mapping_end_uses()

# tic0 - the tic for the toc at the end of the script
tic0 = datetime.datetime.now()

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

