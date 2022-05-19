import json
import pandas as pd
import numpy as np

################################################################################
def isfloat(x): # {{{
    try:
        float(x)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

# }}}

################################################################################
def json_to_df(data = None, path = None): #{{{

    assert bool(data is not None) ^ bool(path is not None)

    if path is not None:
        f = open(path, "r")
        data = json.load(f)
        f.close()

    x = flatten_dict(data)
    x = [(*a, str(b)) for a,b in x.items()]
    x = pd.DataFrame(x)
    x.columns = ["lvl" + str(i) for i in range(len(x.columns))]
    return x
# }}}

################################################################################
def flatten_dict(nested_dict): #{{{
    res = {}
    if isinstance(nested_dict, dict):
        for k in nested_dict:
            flattened_dict = flatten_dict(nested_dict[k])
            for key, val in flattened_dict.items():
                key = list(key)
                key.insert(0, k)
                res[tuple(key)] = val
    else:
        res[()] = nested_dict
    return res
# }}}

################################################################################
class mapping_variables: # {{{

    def __init__(self):
        self.building_type_to_class =\
                pd.DataFrame(data = {
                      "assembly"           : "Commercial"
                    , "education"          : "Commercial"
                    , "food sales"         : "Commercial"
                    , "food service"       : "Commercial"
                    , "health care"        : "Commercial"
                    , "lodging"            : "Commercial"
                    , "large office"       : "Commercial"
                    , "small office"       : "Commercial"
                    , "mercantile/service" : "Commercial"
                    , "warehouse"          : "Commercial"
                    , "other"              : "Commercial"
                    , "single family home" : "Residential"
                    , "multi family home"  : "Residential"
                    , "mobile home"        : "Residential"
                    }.items(),
                    columns = ["building_type", "building_class"]
                    )

        self.end_uses =\
                pd.DataFrame(data = {
                      "Cooking"                   : "Appliances"
                    , "Cooling (Env.)"            : np.nan
                    , "Cooling (Equip.)"          : "Cooling"
                    , "Computers and Electronics" : "Other"
                    , "Heating (Env.)"            : np.nan
                    , "Heating (Equip.)"          : "Heating"
                    , "Lighting"                  : "Lighting"
                    , "Other"                     : "Other"
                    , "Refrigeration"             : "Appliances"
                    , "Ventilation"               : np.nan
                    , "Water Heating"             : "Appliances"
                    }.items(),
                    columns = ["end_use", "emf_end_use"]
                    )

        self.building_class_construction =\
                pd.DataFrame.from_dict(data = {
                    "Commercial (Existing)"  : {
                        "building_class" : "Commercial",
                        "building_construction" : "Existing"
                        },
                    "Commercial (New)": {
                        "building_class" : "Commercial",
                        "building_construction" : "New"
                        },
                    "Residential (Existing)" : {
                        "building_class" : "Residential",
                        "building_construction" : "Existing"
                        },
                    "Residential (New)": {
                        "building_class" : "Residential",
                        "building_construction" : "New"
                        }
                    }, orient = "index")\
                            .reset_index()\
                            .rename(columns = {"index" : "building_class0"})


    def info(self):
        print("A collection of DataFrames to map one set of variable values to another.\n" +
              " * building_type_to_class"
              " * building_class_construction"
              " * end_uses"
                )
# }}}
