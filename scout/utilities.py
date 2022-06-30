import json
import pandas as pd
import numpy as np
import gzip

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
        if path.endswith(".gz"):
            with gzip.open(path, 'r') as f:
                file_content = f.read()
            json_str = file_content.decode("utf-8")
            data = json.loads(json_str)
        else:
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

        self.direct_indirect_fuel =\
                pd.DataFrame(data = {
                    "Natural Gas"      : "Direct",
                    "Distillate/Other" : "Direct",
                    "Biomass"          : "Direct",
                    "Propane"          : "Direct",
                    "Electric"         : "Indirect",
                    "Non-Electric"     : "Indirect"
                    }.items(),
                    columns = ["fuel_type", "direct_indirect_fuel"]
                    )

        self.emf_base_string =\
                pd.DataFrame(data = {
                    "Avoided CO\u2082 Emissions (MMTons)" : "*Emissions|CO2|Energy|Demand|Buildings",
                    "Energy Savings (MMBtu)"              : "*Final Energy|Buildings"
                    }.items(),
                    columns = ["impact", "emf_base_string"]
                    )

        self.fuel_types =\
                pd.DataFrame(data = {
                    "Natural Gas"      : "Gas",
                    "Propane"          : "Gas",
                    "Distillate/Other" : "Oil",
                    "Biomass"          : "Biomass Solids",
                    "Electric"         : "Electricity",
                    "Electricity"      : "Electricity"
                    }.items(),
                    columns = ["fuel_type", "emf_fuel_type"]
                    )

    def info(self):
        print("A collection of DataFrames to map one set of variable values to another.\n" +
              " * building_type_to_class" +
              " * building_class_construction" +
              " * direct_indirect_fuel" +
              " * end_uses" +
              " * emf_base_string " +
              " * fuel_types "
                )
# }}}

################################################################################
class conversion_data: # {{{
    def __init__(self, version = ""): # {{{

        assert version in ["", "ce", "gsref", "decarb", "decarb_lite"]

        self.path = "supporting_data/convert_data/site_source_co2_conversions" + version + ".json"
        df = json_to_df(path = self.path)
        self.aeo_year = int(df.lvl1[df.lvl0 == "updated_to_aeo_year"].values[0])
        self.aeo_case = str(df.lvl1[df.lvl0 == "updated_to_aeo_case"].values[0])
        self.calc_method = str(df.lvl1[df.lvl0 == "site-source calculation method"].values[0])
        #
        self.units_sources = df[(df.lvl1 == "units") | (df.lvl1 == "source") | (df.lvl2 == "units") | (df.lvl2 == "source")][["lvl0", "lvl1", "lvl2", "lvl3"]]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl3"] = self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl2"]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl2"] = self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl1"]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl1"] = np.nan
        #
        self.data = df.loc[df.lvl2 == "data"][["lvl0", "lvl1", "lvl3", "lvl4", "lvl5"]]
        idx = ~((self.data.lvl3 == "residential") | (self.data.lvl3 == "commercial"))
        self.data.loc[idx, "lvl5"] = self.data.loc[idx, "lvl4"]
        self.data.loc[idx, "lvl4"] = self.data.loc[idx, "lvl3"]
        self.data.loc[idx, "lvl3"] = np.nan
        self.data.columns = ["fuel", "impact", "rescom", "year", "value"]
        self.data.value = self.data.value.apply(float)
        self.data.year  = self.data.year.apply(int)
    # }}}

    def info(self): # {{{
        print(f"path:                           {self.path}")
        print(f"basename:                       {self.basename}")
        print(f"aeo_year:                       {self.aeo_year}")
        print(f"aeo_case:                       {self.aeo_case}")
        print(f"site-source calculation method: {self.calc_method}")
        print(f"units_sources:                  a DataFrame")
        print(f"data:                           a DataFrame")
    # }}}
# }}}

################################################################################
#                                 End of File                                  #
################################################################################

