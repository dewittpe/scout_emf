################################################################################
import json
import pandas as pd
import re
import datetime
import numpy as np
import copy
from collections import defaultdict

f = open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm", "r")
baseline = json.load(f)
f.close()

#f = open("./supporting_data/stock_energy_tech_data/mseg_res_com_emm_pretty.json", "w")
#json.dump(baseline, f, indent = 12)


# Function Definitions
def depth(x): # {{{
    """
    find the depth of dictionary or list

    Args
      x : a dict or list

    Return and integer
    """

    if isinstance(x, dict) and x:
        return 1 + max(depth(x[a]) for a in x)
    elif isinstance(x, list) and x:
        return 1 + max(depth(a) for a in x)
    else:
        return 0
#}}}

def unique(list1): # {{{
    unique_list = []
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)

    for x in unique_list:
        print(x)

# }}}

def isfloat(x): # {{{
    try:
        float(x)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

# }}}
 
def isyear(x) : # {{{
    try:
        l = len(x)
        f = float(x)
        i = int(x)
        if ((int(f) == i) and (l == 4)):
            return True
        else :
            return False
    except ValueError:
        return False
    except TypeError:
        return False
# }}}

def json_to_df(x) : # {{{
    try:
        dpth = depth(x)
        assert dpth <= 8
    except AssertionError:
        print(f"json_to_df has been built to support nested dict to 8 levels of depth, the dict you've passed has a max depth of {dpth}.")
    else:
        return json_to_df_worker(x)

# }}}

def json_to_df_worker(x): #{{{
    keys = []
    for lvl0 in x.keys():
        d = {"lvl0" : lvl0}
        if not isinstance(x[lvl0], dict):
            d["lvl1"] = x[lvl0]
            keys.append(d)
        else:
            for lvl1 in x[lvl0].keys():
                d = {"lvl0" : lvl0, "lvl1" : lvl1}
                if not isinstance(x[lvl0][lvl1], dict):
                    d["lvl2"] = x[lvl0][lvl1]
                    keys.append(d)
                else:
                    for lvl2 in x[lvl0][lvl1].keys():
                        d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2}
                        if not isinstance(x[lvl0][lvl1][lvl2], dict):
                            d["lvl3"] = x[lvl0][lvl1][lvl2]
                            keys.append(d)
                        else:
                            for lvl3 in x[lvl0][lvl1][lvl2].keys():
                                d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3}
                                if not isinstance(x[lvl0][lvl1][lvl2][lvl3], dict):
                                    d["lvl4"] = x[lvl0][lvl1][lvl2][lvl3]
                                    keys.append(d)
                                else:
                                    for lvl4 in x[lvl0][lvl1][lvl2][lvl3].keys():
                                        d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3, "lvl4": lvl4}
                                        if not isinstance(x[lvl0][lvl1][lvl2][lvl3][lvl4], dict):
                                            d["lvl5"] = x[lvl0][lvl1][lvl2][lvl3][lvl4]
                                            keys.append(d)
                                        else:
                                            for lvl5 in x[lvl0][lvl1][lvl2][lvl3][lvl4].keys():
                                                d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3, "lvl4": lvl4, "lvl5" : lvl5}
                                                if not isinstance(x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5], dict):
                                                    d["lvl6"] = x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5]
                                                    keys.append(d)
                                                else:
                                                    for lvl6 in x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5].keys():
                                                        d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3, "lvl4": lvl4, "lvl5" : lvl5, "lvl6" : lvl6}
                                                        if not isinstance(x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6], dict):
                                                            d["lvl7"] = x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6]
                                                            keys.append(d)
                                                        else:
                                                            for lvl7 in x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6].keys():
                                                                d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3, "lvl4": lvl4, "lvl5" : lvl5, "lvl6" : lvl6, "lvl7" : lvl7}
                                                                if not isinstance(x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6][lvl7], dict):
                                                                    d["lvl8"] = x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6][lvl7]
                                                                    keys.append(d)
                                                                else:
                                                                    for lvl8 in x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6][lvl7].keys():
                                                                        d = {"lvl0" : lvl0, "lvl1" : lvl1, "lvl2" : lvl2, "lvl3" : lvl3, "lvl4": lvl4, "lvl5" : lvl5, "lvl6" : lvl6, "lvl7" : lvl7, "lvl8" : lvl8}
                                                                        if not isinstance(x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6][lvl7][lvl8], dict):
                                                                            d["lvl9"] = x[lvl0][lvl1][lvl2][lvl3][lvl4][lvl5][lvl6][lvl7][lvl8]
                                                                            keys.append(d)
                                                                        else:
                                                                            print("UNEXPECTED DEPTH")
    return keys
# }}}

keys = json_to_df(baseline)
keys_df = pd.DataFrame.from_dict(keys)
print(keys_df)




################################################################################
# HOW TO GET USEFUL DATA??????


# Example issue to deal with, stock vs energy, appear in multiple levels

any(keys_df.lvl0 == "stock") # False
any(keys_df.lvl1 == "stock") # False
any(keys_df.lvl2 == "stock") # False
any(keys_df.lvl3 == "stock") # False
any(keys_df.lvl4 == "stock") # True
any(keys_df.lvl5 == "stock") # True
any(keys_df.lvl6 == "stock") # True
any(keys_df.lvl7 == "stock") # False
any(keys_df.lvl8 == "stock") # False



keys_df
# lvl0: Region
# lvl1: building_type
# lvl2: 
#   one of two things: 
#   1. building type metadata
#   2. fuel_type
#
# lvl3: 
#   if lvl2 is building type metadata then lvl3 the year (lvl4 value)
#   if lvl2 is fuel type lvl3 is _always_ end_use
#
# lvl4: 
#   One of four things:
#   1. values if lvl2 was building metadata
#   2. if lvl2 is fuel type then
#      a. supply/demand key if lvl3 is a heating or cooling end use  (includes secondary heating)
#      b. technology_type or
#      c. stock/energy keys
#
# lvl5
#   if (lvl4 = 2a) then technology_type / envelope components
#   if (lvl4 = 2b) then stock/energy keys
#   if (lvl4 = 2c) year or NA
#
# lvl6
#   if (lvl4 = 2c) value
#   if (lvl5 is stock/energy key) then NA or year
#   if (lvl5 is technology_type / envelope components) then stock/energy key
#
# lvl7 
#   values or years
#
# lvl8 
#   values



#keys_df[keys_df.lvl3 == "secondary heating"]
#
#keys_df[keys_df.lvl4 == "water services"]
#keys_df[keys_df.lvl4 == "telecom systems"]



################################################################################
#                                 End of File                                  #
################################################################################

