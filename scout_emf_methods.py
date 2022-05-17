################################################################################
# file: scout_emf_methods.py
#
# Define methods for simplifying importing the ECM results, baseline values,
# conversion metrics, and building of graphics for Scout EMF.
#
# Methods Defined herein:
#
#
#
################################################################################
import json
import pandas as pd
import numpy as np
import warnings
import re
import datetime
import os
from collections import defaultdict


################################################################################
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

################################################################################
def import_ecm_results(path): # {{{
    df = json_to_df(path)
    assert any(df.lvl0 == "On-site Generation")

    # split the data set into several smaller data frames,
    # 1. On-site Generation
    # 2. ECMs
    #    a. Filter Variables
    #    b. Markets and Savings
    #    c.
    on_site_generation = df[df.lvl0 == "On-site Generation"]
    ecms               = df[df.lvl0 != "On-site Generation"]
    ecms = ecms.rename(columns = {"lvl0" : "ecm"})
    filter_variables   = ecms[ecms.lvl1 == "Filter Variables"]
    ecms               = ecms[ecms.lvl1 != "Filter Variables"]

    ############################################################################
    # clean up the on-site generation data frame
    assert all(on_site_generation.lvl7.isna())
    assert all(on_site_generation.lvl8.isna())
    assert all(on_site_generation.lvl9.isna())
    on_site_generation = on_site_generation.drop(columns = ["lvl0", "lvl7", "lvl8", "lvl9"])

    # verify that the "Overall" sums are equivalent to the sum over the regions
    # and building type
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl6"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"]
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl5"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"]

    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"] = None
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"] = None

    on_site_generation.lvl6 = on_site_generation.lvl6.apply(float)

    x = on_site_generation\
            .groupby(["lvl1", "lvl2", "lvl5"])\
            .agg({"lvl6" : "sum"})
    x.reset_index(inplace = True)
    x = x.pivot(index = ["lvl1", "lvl5"], columns = ["lvl2"], values = ["lvl6"])
    x.reset_index(inplace = True)
    x["abs_delta"] = abs(x.lvl6["By Category"] - x.lvl6["Overall"])

    #print(x[x.abs_delta > 1e-8])
    #assert all(x["abs_delta"] < 1e-8)
    if any(x.abs_delta < 1e-8):
        warnings.warn("At least one on_site_generation aggregation differs from 'Overall' value.")

    # only return the "by category" data as the "overall" is redundant
    on_site_generation = on_site_generation[on_site_generation.lvl2 == "By Category"]
    on_site_generation = on_site_generation.drop(columns = ["lvl2"])

    # rename columns in the on_site_generation frame for human ease of use
    on_site_generation.rename(columns = {
        "lvl1" : "metric",
        "lvl3" : "region",
        "lvl4" : "building_type",
        "lvl5" : "year",
        "lvl6" : "value"},
        inplace = True)

    # set data types
    assert all(on_site_generation.value.apply(isfloat))
    on_site_generation.value = on_site_generation.value.apply(float)

    assert all(on_site_generation.year.str.contains(r"^\d{4}$"))
    on_site_generation.year = on_site_generation.year.apply(int)

    ############################################################################
    # clean up filter_variables
    filter_variables = filter_variables.pivot(index = ["ecm"],
            columns = ["lvl2"],
            values  = ["lvl3"])

    filter_variables = filter_variables.reset_index(col_level = 1)
    filter_variables.columns = filter_variables.columns.map(lambda t: t[1])

    ############################################################################
    # markets_and_savings
    #
    # Ignore the Markets and Savings (Overall), no need to import aggregated
    # data
    ecm_mas = ecms[ecms.lvl1 == "Markets and Savings (by Category)"]
    ecm_mas = ecm_mas.drop(columns = ["lvl1"])
    ecm_mas = ecm_mas.rename(columns = {
        "lvl2" : "scenario",
        "lvl3" : "metric",
        "lvl4" : "region",
        "lvl5" : "building_class",
        "lvl6" : "end_use",
        "lvl7" : "fuel_type",
        "lvl8" : "year",
        "lvl9" : "value"
        })

    # verify assumption that all fuel_types are defined
    assert all(ecm_mas.fuel_type.notna())

    # move data from one column to another as needed
    idx = ecm_mas.fuel_type.str.contains("^\d{4}$")
    ecm_mas.loc[idx, "value"]     = ecm_mas.loc[idx, "year"]
    ecm_mas.loc[idx, "year"]      = ecm_mas.loc[idx, "fuel_type"]
    ecm_mas.loc[idx, "fuel_type"] = "Not Applicable"

    # set data types
    assert all(ecm_mas.value.apply(isfloat))
    ecm_mas.value = ecm_mas.value.apply(float)

    assert all(ecm_mas.year.str.contains("^\d{4}$"))
    ecm_mas.year = ecm_mas.year.apply(int)

    ############################################################################
    # financial_metrics
    financial_metrics = ecms[ecms.lvl1 == "Financial Metrics"]
    financial_metrics = financial_metrics[["ecm", "lvl2", "lvl3", "lvl4"]]
    financial_metrics = financial_metrics.rename(columns =
            {"lvl2" : "metric", "lvl3" : "year", "lvl4" : "value"})

    # set data types
    assert all(financial_metrics.value.apply(isfloat))
    financial_metrics.value = financial_metrics.value.apply(float)

    assert all(financial_metrics.year.str.contains("^\d{4}$"))
    financial_metrics.year = financial_metrics.year.apply(int)

    ############################################################################
    # return a tuple of data frames
    return ecm_mas, financial_metrics, filter_variables, on_site_generation

# }}}

################################################################################
def import_baseline(path): # {{{
    """
    Import Baseline data

    Per conversation with Chioke this is the outline of the structure of
    baseline json file
        lvl0: Region
        lvl1: building_type
        lvl2:
          one of two things:
          1. building type metadata
          2. fuel_type

        lvl3:
          if lvl2 is building type metadata then lvl3 the year (lvl4 value)
          if lvl2 is fuel type lvl3 is _always_ end_use

        lvl4:
          One of four things:
          1. values if lvl2 was building metadata
          2. if lvl2 is fuel type then
             a. supply/demand key if lvl3 is a heating or cooling end use
                (includes secondary heating)
             b. technology_type or
             c. stock/energy keys

        lvl5
          if (lvl4 = 2a) then technology_type / envelope components
          if (lvl4 = 2b) then stock/energy keys
          if (lvl4 = 2c) year or NA

        lvl6
          if (lvl4 = 2c) value
          if (lvl5 is stock/energy key) then NA or year
          if (lvl5 is technology_type / envelope components) then stock/energy
             key

        lvl7
          values or years

        lvl8
          values
    """

    df = json_to_df(path)
    df = df.rename(columns = {"lvl0" : "region", "lvl1" : "building_type"})
    df = pd.merge(df, map_building_type_to_class(),
            how = "left",
            on = "building_type")

    assert all(df.building_class.notna())

    # split into two data frame
    bt_metadata = df[df.lvl5.isna()]
    df = df[df.lvl5.notna()]

    ############################################################################
    # clean up metadata
    bt_metadata = bt_metadata[["region", "building_type", "building_class", "lvl2", "lvl3", "lvl4"]]
    bt_metadata = bt_metadata.rename(columns =
            {"lvl2" : "metric", "lvl3" : "year", "lvl4" : "value"})

    assert all(bt_metadata.year.str.contains(r"^\d{4}$"))
    bt_metadata.year = bt_metadata.year.apply(int)

    assert all(bt_metadata.value.apply(isfloat))
    bt_metadata.value = bt_metadata.value.apply(float)

    ############################################################################
    # clean up df

    # remove useless rows
    df = df[~((df.lvl6 == "stock") & (df.lvl7 == "NA")) ]
    df = df[~((df.lvl5 == "stock") & (df.lvl6 == "NA")) ]
    df = df[~((df.lvl4 == "stock") & (df.lvl5 == "NA")) ]

    # move values from one column to the next.
    # * lvl8 will have all the "values" __ALL Exajoule__
    # * lvl7 will have all the years
    # * lvl6 will have all stock_energy indicators

    idx = (df.lvl4 == "stock") | (df.lvl4 == "energy")
    df.loc[idx, "lvl8"] = df.loc[idx, "lvl6"]
    df.loc[idx, "lvl7"] = df.loc[idx, "lvl5"]
    df.loc[idx, "lvl6"] = df.loc[idx, "lvl4"]
    df.loc[idx, "lvl5"] = np.nan
    df.loc[idx, "lvl4"] = np.nan

    idx = (df.lvl5 == "stock") | (df.lvl5 == "energy")
    df.loc[idx, "lvl8"] = df.loc[idx, "lvl7"]
    df.loc[idx, "lvl7"] = df.loc[idx, "lvl6"]
    df.loc[idx, "lvl6"] = df.loc[idx, "lvl5"]
    df.loc[idx, "lvl5"] = np.nan

    # if lvl4 is not demand/supply then it is a technology_type and needs to be
    # shifted over to lvl5
    idx = (df.lvl4.notna()) & (df.lvl4 != "demand") & (df.lvl4 != "supply")
    df.loc[idx, "lvl5"] = df.loc[idx, "lvl4"]
    df.loc[idx, "lvl4"] = np.nan

    # rename columns to be human useful
    df = df.rename(columns =
            {
                "lvl2" : "fuel_type",
                "lvl3" : "end_use",
                "lvl4" : "demand_supply",
                "lvl5" : "technology_type",
                "lvl6" : "stock_energy",
                "lvl7" : "year",
                "lvl8" : "Exajoules"
                })

    assert all(df.year.str.contains(r"^\d{4}$"))
    df.year = df.year.apply(int)

    assert all(df.Exajoules.apply(isfloat))
    df.Exajoules = df.Exajoules.apply(float)


    ############################################################################
    # return tuple of data frames
    return bt_metadata, df

# }}}

################################################################################
def map_building_class():                                                   #{{{
    """
    Map for what is really just splitting a string
    """
    d = {
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
            }

    return pd.DataFrame.from_dict(d, orient = "index")\
            .reset_index()\
            .rename(columns = {"index" : "building_class0"})

#}}}

################################################################################
def map_direct_indirect_fuel():                                             #{{{
    """
    Map for fuel type to direct or indirect
    """
    d = {
            "Natural Gas" : "Direct",
            "Distillate/Other" : "Direct",
            "Biomass" : "Direct",
            "Propane" : "Direct",
            "Electric" : "Indirect",
            "Non-Electric" : "Indirect"
            }

    return pd.DataFrame(
            data = d.items(),
            columns = ["fuel_type", "direct_indirect_fuel"]
            )
#}}}

################################################################################
def map_emf_base_string():                                              #{{{
    """
    A data frame to map variable values to base EMF strings

    Arguments:
        None

    Return:
        A pandas DataFrame
    """
    d = {
            "Avoided CO\u2082 Emissions (MMTons)" : "*Emissions|CO2|Energy|Demand|Buildings",
            "Energy Savings (MMBtu)" : "*Final Energy|Buildings"
            }
    return pd.DataFrame(data = d.items(),
            columns = ["metric", "emf_base_string"]
            )
#}}}

################################################################################
def map_fuel_types():                                                       #{{{
    """
    Map for fuel types to emf fuel types
    """
    d = {
            "Natural Gas"      : "Gas",
            "Propane"          : "Gas",
            "Distillate/Other" : "Oil",
            "Biomass"          : "Biomass Solids",
            "Electric"         : "Electricity",
            "Electricity"      : "Electricity"
            }
    return pd.DataFrame(data = d.items(),
            columns = ["fuel_type", "emf_fuel_type"]
            )
#}}}

################################################################################
def map_end_uses():                                                         #{{{
    """
    Map for end uses
    """
    d = {
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
            }
    return pd.DataFrame(data = d.items(), columns = ["end_use", "emf_end_use"])
#}}}

################################################################################
def map_building_type_to_class():                                           #{{{

    d = {
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
            }

    return pd.DataFrame(data = d.items(),
            columns = ["building_type", "building_class"]
            )

# }}}

################################################################################
def ecm_results_to_emf_aggregation(df):                                    # {{{
    """
    Aggregate ECM Results to EMF format

    Args: a data frame that was returned by import_ecm_results
    """

    # add emf_base_string and subset to only the rows with an emf_base_string
    df = pd.merge(df, map_emf_base_string(), how = "inner", on = "metric")

    # map building classes
    df = pd.merge(df, map_building_class(),
            how = "left",
            left_on = "building_class",
            right_on = "building_class0",
            suffixes = ('_x', '')
            )
    df = df.drop(columns = ["building_class0", "building_class_x"])

    # map fuel types
    df = pd.merge(df, map_fuel_types(), how = "left", on = "fuel_type")
    if any(df.emf_fuel_type.isna()):
        not_mapped = set(df[df.emf_fuel_type.isna()]["fuel_type"])
        msg = ", ".join(not_mapped)
        warnings.warn("Fuel types not mapped to EMF fuel types: " + msg)

    # map direct_indirect fuel
    df = pd.merge(df, map_direct_indirect_fuel(), how = "left", on = "fuel_type")
    if any(df.direct_indirect_fuel.isna()):
        not_mapped = set(df[df.direct_indirect_fuel.isna()]["fuel_type"])
        msg = ", ".join(not_mapped)
        warnings.warn("Fuel Types not mapped to direct/indirect: " + msg)

    # map end uses
    df = pd.merge(df, map_end_uses(), how = "left", on = "end_use")
    if any(df.emf_end_use.isna()):
        not_mapped = set(df[df.emf_end_use.isna()]["end_use"])
        msg = ", ".join(not_mapped)
        warnings.warn(f"Unmapped end uses: " + msg)

    # Convert MMBtu to Exajoules
    idx = df.metric.str.contains("MMBtu")
    df.loc[idx, "value"] *= 1.05505585262e-9
    df.metric = df.metric.str.replace("MMBtu", "EJ")

    # Aggregations
    # NOTE: units for the value column are unique between the emf_base_strings.
    # This is okay and accounted for since all aggregations are done, in part,
    # with a groupby emf_base_string.
    a0 = df\
            .groupby(["region", "emf_base_string", "year"])\
            .agg(value = ("value", "sum"))

    a1 = df\
            .groupby(["region", "emf_base_string", "building_class", "year"])\
            .agg(value = ("value", "sum"))

    a2 = df\
            .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "year"])\
            .agg(value = ("value", "sum"))

    a3_0 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["region", "emf_base_string", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))
    a3_1 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["region", "emf_base_string", "building_class", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))
    a3_2 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))

    a4_0 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["region", "emf_base_string", "emf_fuel_type", "year"])\
            .agg(value = ("value", "sum"))
    a4_1 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["region", "emf_base_string", "building_class", "emf_fuel_type", "year"])\
            .agg(value = ("value", "sum"))
    a4_2 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "emf_fuel_type", "year"])\
            .agg(value = ("value", "sum"))

    # Aggregation clean up
    a0.reset_index(inplace = True)
    a1.reset_index(inplace = True)
    a2.reset_index(inplace = True)
    a3_0.reset_index(inplace = True)
    a3_1.reset_index(inplace = True)
    a3_2.reset_index(inplace = True)
    a4_0.reset_index(inplace = True)
    a4_1.reset_index(inplace = True)
    a4_2.reset_index(inplace = True)

    # build the full emf_string
    a0["emf_string"] = a0.region + a0.emf_base_string
    a1["emf_string"] = a0.region + a1.emf_base_string + "|" + a1.building_class
    a2["emf_string"] = a0.region + a2.emf_base_string + "|" + a2.building_class + "|" + a2.emf_end_use

    a3_0["emf_string"] = a3_0.region + a3_0.emf_base_string + "|" + a3_0.direct_indirect_fuel
    a3_1["emf_string"] = a3_1.region + a3_1.emf_base_string + "|" + a3_1.building_class + "|" + a3_1.direct_indirect_fuel
    a3_2["emf_string"] = a3_2.region + a3_2.emf_base_string + "|" + a3_2.building_class + "|" + a3_2.emf_end_use + "|" + a3_2.direct_indirect_fuel

    a4_0["emf_string"] = a4_0.region + a4_0.emf_base_string + "|" + a4_0.emf_fuel_type
    a4_1["emf_string"] = a4_1.region + a4_1.emf_base_string + "|" + a4_1.building_class + "|" + a4_1.emf_fuel_type
    a4_2["emf_string"] = a4_2.region + a4_2.emf_base_string + "|" + a4_2.building_class + "|" + a4_2.emf_end_use + "|" + a4_2.emf_fuel_type

    # build one data frame with all the aggregations
    a = pd.concat([
        a0[["emf_string", "year", "value"]],
        a1[["emf_string", "year", "value"]],
        a2[["emf_string", "year", "value"]],
        a3_0[["emf_string", "year", "value"]],
        a3_1[["emf_string", "year", "value"]],
        a3_2[["emf_string", "year", "value"]],
        a4_0[["emf_string", "year", "value"]],
        a4_1[["emf_string", "year", "value"]],
        a4_2[["emf_string", "year", "value"]]
        ])
    a.year = a.year.apply(str) # this is needed so the column names post pivot are strings
    a = a.pivot_table(index = ["emf_string"], columns = ["year"], values = ["value"])
    a.columns = a.columns.droplevel(0)
    a.reset_index(inplace = True)

    return df, a

# }}}




class conversion_data:
    def __init__(self, path):
        self.basename = os.path.basename(path)

        assert self.basename in [
                "site_source_co2_conversions-ce.json",
                "site_source_co2_conversions-decarb.json",
                "site_source_co2_conversions-decarb_lite.json",
                "site_source_co2_conversions-gsref.json",
                "site_source_co2_conversions.json",
                ]

        self.path = path
        df = json_to_df(path)
        self.aeo_year = int(df.lvl1[df.lvl0 == "updated_to_aeo_year"].values[0])
        self.aeo_case = str(df.lvl1[df.lvl0 == "updated_to_aeo_case"].values[0])
        self.calc_method = str(df.lvl1[df.lvl0 == "site-source calculation method"].values[0])
        #
        self.units_sources = df[(df.lvl1 == "units") | (df.lvl1 == "source") | (df.lvl2 == "units") | (df.lvl2 == "source")][["lvl0", "lvl1", "lvl2", "lvl3"]]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl3"] = self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl2"]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl2"] = self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl1"]
        self.units_sources.loc[self.units_sources.lvl0 == "CO2 price", "lvl1"] = None
        #
        self.data = df.loc[df.lvl2 == "data"][["lvl0", "lvl1", "lvl3", "lvl4", "lvl5"]]
        idx = ~((self.data.lvl3 == "residential") | (self.data.lvl3 == "commercial"))
        self.data.loc[idx, "lvl5"] = self.data.loc[idx, "lvl4"]
        self.data.loc[idx, "lvl4"] = self.data.loc[idx, "lvl3"]
        self.data.loc[idx, "lvl3"] = None
        self.data.columns = ["fuel", "metric", "rescom", "year", "value"]
        self.data.value = self.data.value.apply(float)
        self.data.year  = self.data.year.apply(int)

    def info(self):
        print(f"path:                           {self.path}")
        print(f"basename:                       {self.basename}")
        print(f"aeo_year:                       {self.aeo_year}")
        print(f"aeo_case:                       {self.aeo_case}")
        print(f"site-source calculation method: {self.calc_method}")
        print(f"units_sources:                  a DataFrame")
        print(f"data:                           a DataFrame")















################################################################################
def unit_conversions():                                                    # {{{
    # MMBtu - Million Metric British Thermal Unit
    # quad  - quadrilion (1e15) BTU  -- million million metric Btu
    # EJ    - Exajoule = 1e18 joule
    # GJ    - gigajoule
    # kg    - kilograms
    # t     - metric ton (1000 kg)
    # Mt    - metric megaton (1,000,000 t)
    MMBtu_to_EJ = 1.05505585262e-9
    MMBtu_to_GJ = 1.05505585262

    quad_to_EJ = 1.055
    EJ_to_quad = 0.94781707774915

    # coversions for different fuels from
    # https://www.eia.gov/environment/emissions/co2_vol_mass.php
    #
    # This web page reports kg CO2 per MMBtu, which is numerically equivlanent
    # to metric megatons of CO2 per quad:
    #
    #   kg CO2                1 Mt            Mt CO2
    #   ------------ x ----------------- =  ------------
    #   MMBtu          1000000 x 1000 kg        quad
    #
    # propane     : 62.88 kg CO2 per MMBtu
    # kerosene    : 73.19 kg CO2 per MMBtu
    # natural gas : 52.91 kg CO2 per MMBtu
    # diesel and home heating fuel (distillate fuel oil) : 74.14 kg CO2 per MMBtu
    # 
    # 95.74, 

# }}}








################################################################################
def convert_energy_to_co2(coefs, verbose = True):                           #{{{
    """
    Convert energy in exajoules to metric tonne of CO2

    Args:
        coef: the pandas DataFrame returned from import_conversion_coeffs
        verbose: report timing
    Return:
        a pandas DataFrame
    """
    # conversion factors
    # EJ = exajoule = 1e18 joules
    # Mt = megatonne
    MMBtu_to_EJ           = 1.05505585262e-9
    EJ_to_quad            = 0.9478
    EJ_to_Mt_co2_propane  = EJ_to_quad * 62.88
    EJ_to_Mt_co2_kerosene = EJ_to_quad * 73.38
    EJ_to_Mt_co2_gas      = EJ_to_quad * 53.056
    EJ_to_Mt_co2_oil      = EJ_to_quad * 74.14
    EJ_to_Mt_co2_bio      = EJ_to_quad * 96.88
    pound_to_Mt           = 0.000453592
    EJ_to_twh             = 277.778

    conversion_factors =\
            {'fuel_type' : ["Electricity", "Gas_lpg", "Gas", "Oil_kerosene",
                "Oil", "Biomass"],
             'coef' : [EJ_to_twh, EJ_to_Mt_co2_propane, EJ_to_Mt_co2_gas,
                 EJ_to_Mt_co2_kerosene, EJ_to_Mt_co2_oil, EJ_to_Mt_co2_bio]
            }
    conversion_factors = pd.DataFrame(data = conversion_factors)

    coefs = coefs.loc[coefs.concept == "CO2 intensity of electricity",
            ["concept", "units", "region", "year", "value"]]



    #coeffs_emm = conv_coefficients[conv_coefficients.index == emm].values[0]
    #for i in final_df.index:
    #    if (emm in i) and ('Electricity' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * coeffs_emm * EJ_to_twh
    #    if (emm in i) and ('Gas_lpg' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * EJ_to_Mt_co2_propane
    #    elif (emm in i) and ('Gas' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * EJ_to_Mt_co2_gas
    #    if (emm in i) and ('Oil_kerosene' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * EJ_to_Mt_co2_kerosene
    #    elif (emm in i) and ('Oil' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * EJ_to_Mt_co2_oil
    #    elif (emm in i) and ('Biomass' in i):
    #        final_df.loc[dict_energy_emissions[i]] = (final_df[final_df.index==i].values[0]) * EJ_to_Mt_co2_bio

    return conversion_factors

# end of convert_energy_to_co2 }}}

################################################################################
def import_conversion_coeffs(path, verbose = True):                         #{{{
    tic = datetime.datetime.now()

    f = open(path, "r")
    d = json.load(f)
    f.close()

    co2 = [{
        "updated_to_aeo_case" : d["updated_to_aeo_case"],
        "updated_to_aeo_year" : d["updated_to_aeo_year"],
        "concept"             : "CO2 intensity of electricity",
        "source"              : d["CO2 intensity of electricity"]["source"],
        "region"              : region,
        "year"                : year,
        "units"               : d["CO2 intensity of electricity"]["units"],
        "value"               : value
        }\
                for region in list(d["CO2 intensity of electricity"]["data"])\
                for year   in list(d["CO2 intensity of electricity"]["data"][region])\
                for value  in     [d["CO2 intensity of electricity"]["data"][region][year]]
                ]
    co2 = pd.DataFrame.from_dict(co2)

    price = [{
        "updated_to_aeo_case" : d["updated_to_aeo_case"],
        "updated_to_aeo_year" : d["updated_to_aeo_year"],
        "concept"             : "End-use electricity price",
        "source"              : d["End-use electricity price"]["source"],
        "building_class"      : bc,
        "region"              : region,
        "year"                : year,
        "units"               : d["End-use electricity price"]["units"],
        "value"               : value
        }\
                for bc     in list(d["End-use electricity price"]["data"])\
                for region in list(d["End-use electricity price"]["data"][bc])\
                for year   in list(d["End-use electricity price"]["data"][bc][region])\
                for value  in     [d["End-use electricity price"]["data"][bc][region][year]]
                ]
    price = pd.DataFrame.from_dict(price)

    rtn = pd.concat([co2, price])

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a DataFrame in {time_delta}")

    return rtn

# }}}

################################################################################
#                                 End of File                                  #
################################################################################

