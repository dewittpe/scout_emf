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
def json_to_df(path): #{{{
    f = open(path, "r")
    x = json.load(f)
    f.close()

    x = flatten_dict(x)
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
