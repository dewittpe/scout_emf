import json
import pandas as pd

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
                    "assembly" : "Commercial",
                    "education" : "Commercial",
                    "food sales" : "Commercial",
                    "food service" : "Commercial",
                    "health care" : "Commercial",
                    "lodging" : "Commercial",
                    "large office" : "Commercial",
                    "small office" : "Commercial",
                    "mercantile/service" : "Commercial",
                    "warehouse" : "Commercial",
                    "other" : "Commercial",
                    "single family home" : "Residential",
                    "multi family home" : "Residential",
                    "mobile home" : "Residential"
                    }.items(),
                    columns = ["building_type", "building_class"]
                    )

    def info(self):
        print("A collection of DataFrames to map one set of variable values to another.\n" +
              " * building_type_to_class"
                )
# }}}
