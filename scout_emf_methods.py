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
def json_to_df(path) : # {{{
    f = open(path, "r")
    x = json.load(f)
    f.close()

    try:
        dpth = depth(x)
        assert dpth <= 9
    except AssertionError:
        print(f"json_to_df has been built to support nested dict to 9 levels of depth, the dict you've passed has a max depth of {dpth}.")
    else:
        return json_to_df_worker(x)

# }}}

################################################################################
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
    return pd.DataFrame.from_dict(keys)
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

    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"] = np.nan
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"] = np.nan

    x = on_site_generation\
            .groupby(["lvl1", "lvl2", "lvl5"])\
            .agg({"lvl6" : "sum"})
    x.reset_index(inplace = True)
    x = x.pivot(index = ["lvl1", "lvl5"], columns = ["lvl2"], values = ["lvl6"])
    x.reset_index(inplace = True)
    assert len(x[(x.lvl6["Overall"].notna()) & (x.lvl6["By Category"] != x.lvl6["Overall"])]) == 0

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

    # split into two data frame
    bt_metadata = df[df.lvl5.isna()]
    df = df[df.lvl5.notna()]

    ############################################################################
    # clean up metadata
    bt_metadata = bt_metadata[["region", "building_type", "lvl2", "lvl3", "lvl4"]]
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
    # * lvl8 will have all the "values"
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
                "lvl8" : "value"
                })

    assert all(df.year.str.contains(r"^\d{4}$"))
    df.year = df.year.apply(int)

    assert all(df.value.apply(isfloat))
    df.value = df.value.apply(float)


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

    # Aggregations
    a0 = df\
            .groupby(["emf_base_string", "year"])\
            .agg(value = ("value", "sum"))

    a1 = df\
            .groupby(["emf_base_string", "building_class", "year"])\
            .agg(value = ("value", "sum"))

    a2 = df\
            .groupby(["emf_base_string", "building_class", "emf_end_use", "year"])\
            .agg(value = ("value", "sum"))

    a3_0 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["emf_base_string", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))
    a3_1 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["emf_base_string", "building_class", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))
    a3_2 = df\
            [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
            .groupby(["emf_base_string", "building_class", "emf_end_use", "direct_indirect_fuel", "year"])\
            .agg(value = ("value", "sum"))

    a4_0 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["emf_base_string", "emf_fuel_type", "year"])\
            .agg(value = ("value", "sum"))
    a4_1 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["emf_base_string", "building_class", "emf_fuel_type", "year"])\
            .agg(value = ("value", "sum"))
    a4_2 = df\
            [df.emf_base_string == "*Final Energy|Buildings"]\
            .groupby(["emf_base_string", "building_class", "emf_end_use", "emf_fuel_type", "year"])\
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

    # A multiplicative factor for energy savings
    a4_0.value *= 1.05505585262e-9
    a4_1.value *= 1.05505585262e-9
    a4_2.value *= 1.05505585262e-9

    # build the full emf_string
    a0["emf_string"] = a0.emf_base_string
    a1["emf_string"] = a1.emf_base_string + "|" + a1.building_class
    a2["emf_string"] = a2.emf_base_string + "|" + a2.building_class + "|" + a2.emf_end_use

    a3_0["emf_string"] = a3_0.emf_base_string + "|" + a3_0.direct_indirect_fuel
    a3_1["emf_string"] = a3_1.emf_base_string + "|" + a3_1.building_class + "|" + a3_1.direct_indirect_fuel
    a3_2["emf_string"] = a3_2.emf_base_string + "|" + a3_2.building_class + "|" + a3_2.emf_end_use + "|" + a3_2.direct_indirect_fuel

    a4_0["emf_string"] = a4_0.emf_base_string + "|" + a4_0.emf_fuel_type
    a4_1["emf_string"] = a4_1.emf_base_string + "|" + a4_1.building_class + "|" + a4_1.emf_fuel_type
    a4_2["emf_string"] = a4_2.emf_base_string + "|" + a4_2.building_class + "|" + a4_2.emf_end_use + "|" + a4_2.emf_fuel_type

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
    a = a.pivot(index = ["emf_string"], columns = ["year"], values = ["value"])
    #a.columns = a.columns.droplevel(0)
    a.reset_index(inplace = True)

    return df, a

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
    EJ_to_quad            = 0.9472
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
def aggregate_ecm_results(df, verbose = True):                              #{{{
    """ Aggregate results for EMF

    Arguments:
        df: a pandas DataFrame returned from import_ecm_results
        verbose: report progress and timing to the user

    Return:
        a pandas DataFrame
    """
    tic = datetime.datetime.now()

    a0 = df\
            .groupby(['emf_string', 'year'])\
            .agg(value=('value','sum'))

    a1 = df\
            .groupby(['emf_string', 'building_class', 'year'])\
            .agg(value=('value','sum'))

    a2 = df\
            .groupby(['emf_string', 'building_class', 'end_use2', 'year'])\
            .agg(value=('value','sum'))

    a3_a0 = df[df.variable == "Avoided CO\u2082 Emissions (MMTons)"]\
            .groupby(['emf_string', 'building_class', 'end_use2', 'direct_fuel', 'year'])\
            .agg(value=('value','sum'))

    a3_a1 = df[df.variable == "Avoided CO\u2082 Emissions (MMTons)"]\
            .groupby(['emf_string', 'direct_fuel', 'year'])\
            .agg(value=('value','sum'))

    a3_a2 = df[df.variable == "Avoided CO\u2082 Emissions (MMTons)"]\
            .groupby(['emf_string', 'building_class', 'direct_fuel', 'year'])\
            .agg(value=('value','sum'))


    a3_e0 = df[df.variable == "Energy Savings (MMBtu)"]\
            .groupby(['emf_string', 'building_class', 'end_use2', 'fuel_type2', 'year'])\
            .agg(value=('value','sum'))

    a3_e1 = df[df.variable == "Energy Savings (MMBtu)"]\
            .groupby(['emf_string', 'building_class', 'fuel_type2', 'year'])\
            .agg(value=('value','sum'))

    a3_e2 = df[df.variable == "Energy Savings (MMBtu)"]\
            .groupby(['emf_string', 'fuel_type2', 'year'])\
            .agg(value=('value','sum'))

    a0.reset_index(inplace = True)
    a1.reset_index(inplace = True)
    a2.reset_index(inplace = True)

    a3_a0.reset_index(inplace = True)
    a3_a1.reset_index(inplace = True)
    a3_a2.reset_index(inplace = True)

    a3_e0.reset_index(inplace = True)
    a3_e1.reset_index(inplace = True)
    a3_e2.reset_index(inplace = True)

    # A multiplicative factor for energy savings
    a3_e0.value *= 1.05505585262e-9
    a3_e1.value *= 1.05505585262e-9
    a3_e2.value *= 1.05505585262e-9

    a1.emf_string = a1.emf_string + "|" + a1.building_class
    a2.emf_string = a2.emf_string + "|" + a2.building_class + "|" + a2.end_use2

    a3_a0.emf_string = a3_a0.emf_string + "|" + a3_a0.building_class + "|" + a3_a0.end_use2 + "|" + a3_a0.direct_fuel
    a3_a1.emf_string = a3_a1.emf_string + "|" + a3_a1.direct_fuel
    a3_a2.emf_string = a3_a2.emf_string + "|" + a3_a2.building_class + "|" + a3_a2.direct_fuel

    a3_e0.emf_string = a3_e0.emf_string + "|" + a3_e0.building_class + "|" + a3_e0.end_use2 + "|" + a3_e0.fuel_type2
    a3_e1.emf_string = a3_e1.emf_string + "|" + a3_e1.building_class + "|" + a3_e1.fuel_type2
    a3_e2.emf_string = a3_e2.emf_string + "|" + a3_e2.fuel_type2

    # one date frame
    a = pd.concat([
                a0[["emf_string", "year", "value"]],
                a1[["emf_string", "year", "value"]],
                a2[["emf_string", "year", "value"]],

                a3_a0[["emf_string", "year", "value"]],
                a3_a1[["emf_string", "year", "value"]],
                a3_a2[["emf_string", "year", "value"]],

                a3_e0[["emf_string", "year", "value"]],
                a3_e1[["emf_string", "year", "value"]],
                a3_e2[["emf_string", "year", "value"]]
            ])
    a = a.pivot(index = ["emf_string"], columns = ["year"], values = ["value"])
    a.columns = a.columns.droplevel(0)
    a.reset_index(inplace = True)

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"Aggregation completed in {time_delta}")

    return a

# end of aggregate_emf }}}

################################################################################
#                                 End of File                                  #
################################################################################

