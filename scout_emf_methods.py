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

################################################################################
class ecm_results:                                                         # {{{
    def __init__(self, path): # {{{
        self.basename = os.path.basename(path)
        self.path = path
        self.df = json_to_df(path)
    # }}}

    def info(self): #{{{
        print(f"path:                           {self.path}")
        print(f"basename:                       {self.basename}")
    #}}}

#}}}

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

