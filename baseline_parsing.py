################################################################################
import json
import pandas as pd
import re
import datetime
import numpy as np
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

################################################################################
# Explore the base line data
depth(baseline)


# build a data frame of key values, and maybe, just maybe, even values?

# Depth level 0  --- REGIONS 
len(baseline)
baseline.keys()
keys_df = pd.DataFrame({"lvl0" : baseline.keys()})

# Depth Level 1 --- Building Type? {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        d = {"lvl0" : k0, "lvl1" : k1}
        keys.append(d)
# }}}

# Depth Level 2 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2}
            keys.append(d)

# }}}

# Depth Level 3 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3}
                keys.append(d)

# }}}

# Depth Level 4 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                if isfloat(baseline[k0][k1][k2][k3]):
                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : baseline[k0][k1][k2][k3]}
                    keys.append(d)
                else:
                    for k4 in baseline[k0][k1][k2][k3].keys():
                        d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4}
                        keys.append(d)

# }}}

# Depth Level 5 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                if isfloat(baseline[k0][k1][k2][k3]):
                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : baseline[k0][k1][k2][k3]}
                    keys.append(d)
                else:
                    for k4 in baseline[k0][k1][k2][k3].keys():
                        if isfloat(baseline[k0][k1][k2][k3][k4]):
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : baseline[k0][k1][k2][k3]}
                            keys.append(d)
                        elif baseline[k0][k1][k2][k3][k4] == "NA":
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : np.nan }
                            keys.append(d)
                        else:
                            for k5 in baseline[k0][k1][k2][k3][k4].keys():
                                d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5}
                                keys.append(d)

# }}}

# Depth Level 6 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                if isfloat(baseline[k0][k1][k2][k3]):
                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : baseline[k0][k1][k2][k3]}
                    keys.append(d)
                else:
                    for k4 in baseline[k0][k1][k2][k3].keys():
                        if isfloat(baseline[k0][k1][k2][k3][k4]):
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : baseline[k0][k1][k2][k3][k4]}
                            keys.append(d)
                        elif baseline[k0][k1][k2][k3][k4] == "NA":
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : np.nan }
                            keys.append(d)
                        else:
                            for k5 in baseline[k0][k1][k2][k3][k4].keys():
                                if isfloat(baseline[k0][k1][k2][k3][k4][k5]):
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : baseline[k0][k1][k2][k3][k4][k5]}
                                    keys.append(d)
                                elif baseline[k0][k1][k2][k3][k4][k5] == "NA":
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : np.nan }
                                    keys.append(d)
                                else:
                                    for k6 in baseline[k0][k1][k2][k3][k4][k5].keys():
                                        d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6}
                                        keys.append(d)

# }}}

# Depth Level 7 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                if isfloat(baseline[k0][k1][k2][k3]):
                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : baseline[k0][k1][k2][k3], "lvl5" : np.nan, "lvl6" : np.nan, "lvl7" : np.nan}
                    keys.append(d)
                else:
                    for k4 in baseline[k0][k1][k2][k3].keys():
                        if isfloat(baseline[k0][k1][k2][k3][k4]):
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : baseline[k0][k1][k2][k3][k4], "lvl6" : np.nan, "lvl7" : np.nan}
                            keys.append(d)
                        elif baseline[k0][k1][k2][k3][k4] == "NA":
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : np.nan , "lvl6" : np.nan, "lvl7" : np.nan}
                            keys.append(d)
                        else:
                            for k5 in baseline[k0][k1][k2][k3][k4].keys():
                                if isfloat(baseline[k0][k1][k2][k3][k4][k5]):
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : baseline[k0][k1][k2][k3][k4][k5], "lvl7" : np.nan}
                                    keys.append(d)
                                elif baseline[k0][k1][k2][k3][k4][k5] == "NA":
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : np.nan, "lvl7" : np.nan }
                                    keys.append(d)
                                else:
                                    for k6 in baseline[k0][k1][k2][k3][k4][k5].keys():
                                        if isfloat(baseline[k0][k1][k2][k3][k4][k5][k6]):
                                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : baseline[k0][k1][k2][k3][k4][k5][k6]}
                                            keys.append(d)
                                        elif baseline[k0][k1][k2][k3][k4][k5][k6] == "NA":
                                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : np.nan }
                                            keys.append(d)
                                        else:
                                            for k7 in baseline[k0][k1][k2][k3][k4][k5][k6].keys():
                                                d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7": k7}
                                                keys.append(d)

# }}}

# Depth Level 8 --- {{{
keys = []
for k0 in baseline.keys():
    for k1 in baseline[k0].keys():
        for k2 in baseline[k0][k1].keys():
            for k3 in baseline[k0][k1][k2].keys():
                if isfloat(baseline[k0][k1][k2][k3]):
                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : baseline[k0][k1][k2][k3]}
                    keys.append(d)
                else:
                    for k4 in baseline[k0][k1][k2][k3].keys():
                        if isfloat(baseline[k0][k1][k2][k3][k4]):
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : baseline[k0][k1][k2][k3][k4]}
                            keys.append(d)
                        elif baseline[k0][k1][k2][k3][k4] == "NA":
                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : np.nan}
                            keys.append(d)
                        else:
                            for k5 in baseline[k0][k1][k2][k3][k4].keys():
                                if isfloat(baseline[k0][k1][k2][k3][k4][k5]):
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : baseline[k0][k1][k2][k3][k4][k5]}
                                    keys.append(d)
                                elif baseline[k0][k1][k2][k3][k4][k5] == "NA":
                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : np.nan}
                                    keys.append(d)
                                else:
                                    for k6 in baseline[k0][k1][k2][k3][k4][k5].keys():
                                        if isfloat(baseline[k0][k1][k2][k3][k4][k5][k6]):
                                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : baseline[k0][k1][k2][k3][k4][k5][k6]}
                                            keys.append(d)
                                        elif baseline[k0][k1][k2][k3][k4][k5][k6] == "NA":
                                            d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : np.nan }
                                            keys.append(d)
                                        else:
                                            for k7 in baseline[k0][k1][k2][k3][k4][k5][k6].keys():
                                                if isfloat(baseline[k0][k1][k2][k3][k4][k5][k6][k7]):
                                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : k7, "lvl8" : baseline[k0][k1][k2][k3][k4][k5][k6][k7]}
                                                    keys.append(d)
                                                elif baseline[k0][k1][k2][k3][k4][k5][k6][k7] == "NA":
                                                    d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7" : k7, "lvl8" : np.nan }
                                                    keys.append(d)
                                                else:
                                                    for k8 in baseline[k0][k1][k2][k3][k4][k5][k6][k7].keys():
                                                        d = {"lvl0" : k0, "lvl1" : k1, "lvl2" : k2, "lvl3" : k3, "lvl4" : k4, "lvl5" : k5, "lvl6" : k6, "lvl7": k7, "lvl8": k8}
                                                        keys.append(d)

# }}}

keys_df = pd.DataFrame.from_dict(keys)
keys_df

print("Are all the lvl8 values floats?  Answer: " + str(all(keys_df.lvl8.apply(isfloat))))
print("Are any the lvl8 values yeara?   Answer: " + str(all(keys_df.lvl8.apply(isyear))))

keys_df[keys_df.lvl7 == "2025"]

################################################################################
# HOW TO GET USEFUL DATA??????


# Example issue to deal with, stock vs energy, appear in multiple levels

any(keys_df.lvl0 == "stock") # No
any(keys_df.lvl1 == "stock") # No
any(keys_df.lvl2 == "stock") # No
any(keys_df.lvl3 == "stock") # No
any(keys_df.lvl4 == "stock") # YES #
any(keys_df.lvl5 == "stock") # YES #
any(keys_df.lvl6 == "stock") # YES #
any(keys_df.lvl7 == "stock") # No


# values at each level
keys_df.groupby(["lvl0"]).size()
keys_df.groupby(["lvl1"]).size()
keys_df.groupby(["lvl2"]).size()
keys_df.groupby(["lvl3"]).size()

# starting with lvl4 there are 'values' so don't consider those
# keys_df.groupby(["lvl4"]).size()

keys_df[(~keys_df.lvl4.apply(isfloat)) | (keys_df.lvl4.apply(isyear))].groupby(["lvl4"]).size()
keys_df[(~keys_df.lvl4.apply(isfloat)) | (keys_df.lvl4.apply(isyear))].groupby(["lvl4"]).size().index

keys_df[(~keys_df.lvl5.apply(isfloat)) | (keys_df.lvl5.apply(isyear))].groupby(["lvl5"]).size()
keys_df[(~keys_df.lvl5.apply(isfloat)) | (keys_df.lvl5.apply(isyear))].groupby(["lvl5"]).size().index

keys_df[(~keys_df.lvl6.apply(isfloat)) | (keys_df.lvl6.apply(isyear))].groupby(["lvl6"]).size()
keys_df[(~keys_df.lvl6.apply(isfloat)) | (keys_df.lvl6.apply(isyear))].groupby(["lvl6"]).size().index

keys_df[(~keys_df.lvl7.apply(isfloat)) | (keys_df.lvl7.apply(isyear))].groupby(["lvl7"]).size()
keys_df[(~keys_df.lvl7.apply(isfloat)) | (keys_df.lvl7.apply(isyear))].groupby(["lvl7"]).size().index

# Looking into lvl0 and lvl1 --- there appears to be a complete set in a cross join sense.
keys_df.groupby(["lvl0", "lvl1"]).count()

keys_df.groupby(["lvl0"]).count()
keys_df.groupby(["lvl0"]).size()

lvl_0_1 = pd.DataFrame(keys_df.groupby(["lvl0", "lvl1"]).size())
lvl_0_1.reset_index(inplace = True)

lvl_0_1.groupby(["lvl0"]).size()
lvl_0_1.groupby(["lvl1"]).size()
all(lvl_0_1.groupby(["lvl0", "lvl1"]).size() == 1)


# what about lvl1 by lvl2
lvl_1_2 = pd.DataFrame(keys_df.groupby(["lvl1", "lvl2"]).size())
lvl_1_2.reset_index(inplace = True)

lvl_1_2.groupby(["lvl1"]).size()
lvl_1_2.groupby(["lvl2"]).size()
all(lvl_1_2.groupby(["lvl0", "lvl1"]).size() == 1)


################################################################################

any((keys_df == "TVs").lvl0) # False
any((keys_df == "TVs").lvl1) # False
any((keys_df == "TVs").lvl2) # False
any((keys_df == "TVs").lvl3) # True
any((keys_df == "TVs").lvl4) # False
any((keys_df == "TVs").lvl5)
any((keys_df == "TVs").lvl6)
any((keys_df == "TVs").lvl7)


# What's a end use?  TVs?  TV, video
keys_df[keys_df.lvl3 == "TVs"]
set(keys_df[keys_df.lvl3 == "TVs"].lvl4)


all(keys_df[keys_df.lvl3 == "TVs"].lvl8.isna())


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



keys_df[keys_df.lvl3 == "secondary heating"]

keys_df[keys_df.lvl4 == "water services"]
keys_df[keys_df.lvl4 == "telecom systems"]



################################################################################
#                                 End of File                                  #
################################################################################

