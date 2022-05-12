################################################################################
# file: scout_emf_methods.py
#
# Define methods for simplifing importing the ECM results, baseline values,
# converstion metrics, and building of graphics for Scout EMF.
#
# Methods Defined herein:
#
# * import_baseline_energy_data
# * import_baseline_building_data
# * import_conversion_coeffs
# * import_ecm_results
#   -- read in the ecm results json and return a DataFrame
#
# * aggregate_emf
# * covert_energy_to_co2
#
################################################################################
import json
import pandas as pd
import numpy as np
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

def import_ecm_results(path):
    df = json_to_df(path)
    assert any(df.lvl0 == "On-site Generation")

    # split the data set into several smaller data frames,
    # 1. On-site Generation
    # 2. ECMs
    #    a. Filter Variables
    #    b.
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

    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl6"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"]
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl5"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"]

    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"] = np.nan
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"] = np.nan

    # verify that the "Overall" sums are equivalent to the sum over the regions
    # and building type
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

    ############################################################################
    # clean up filter_variables
    filter_variables = filter_variables.pivot(index = ["ecm"],
            columns = ["lvl2"],
            values  = ["lvl3"])

    filter_variables = filter_variables.reset_index(col_level = 1)
    filter_variables.columns = filter_variables.columns.map(lambda t: t[1])

    return ecms, filter_variables, on_site_generation











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
def mapping_emf_base_string():                                              #{{{
    """
    A data frame to map variable values to base EMF strings

    Arguments:
        None

    Return:
        A pandas DataFrame
    """
    d = {
            "variable" : ["Avoided CO\u2082 Emissions (MMTons)"
                , "Energy Savings (MMBtu)"]
            , "emf_base_string" : ["*Emissions|CO2|Energy|Demand|Buildings"
                , "*Final Energy|Buildings"
                ]
            }
    return pd.DataFrame(data = d)
#}}}

################################################################################
def mapping_building_class():                                              #{{{
    """
    Map for what is really just splitting a string
    """
    d = {
            "building_class0" : ["Commercial (Existing)", "Commercial (New)"
                , "Residential (Existing)", "Residential (New)"]
            , "building_class" : ["Commercial", "Commercial", "Residential",
            "Residential"]
            , "building_construction" : ["Existing", "New", "Existing", "New"]
            }
    return pd.DataFrame(data = d)
#}}}

################################################################################
def mapping_direct_fuel():                                                  #{{{
    """
    Map for fuel type to direct or indirect
    """
    d = {
            "fuel"         : ['Natural Gas', 'Distillate/Other', 'Biomass', 'Propane', 'Electric', 'Non-Electric']
            , "(in)direct" : ['Direct',      'Direct',           'Direct',  'Direct',  'Indirect', 'Direct']
            }
    return pd.DataFrame(data = d)
#}}}

################################################################################
def mapping_emf_fuel():                                                     #{{{
    """
    Map for fuel types to emf fuel types
    """
    d = {
            "fuel"       : ['Natural Gas', 'Propane', 'Distillate/Other', 'Biomass', 'Electric', 'Electricity']
            , "emf_fuel" : ['Gas',         'Gas',     'Oil',              'Biomass Solids', 'Electricity', 'Electricity']
            }
    return pd.DataFrame(data = d)
#}}}

################################################################################
def mapping_end_uses():                                                     #{{{
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
    return pd.DataFrame(data = d.items(), columns = ["end_use0", "end_use"])
#}}}

################################################################################
def import_ecm_results_v1(path, verbose = True):                            #{{{
    """ Import ECM results

     THIS IS VERY FAST BUT REQUIRES A CONSISTENT JSON FORMAT.  SINCE FUEL TYPE
     MAY NOT ALWAYS EXIST THE LOGIC TO TO BUILD THE NEEDED DATAFRAME WILL SLOW
     DOWN THE PROCESS

    Arguments:
        path: file path to a ecm_results.json file
        verbose : print time required to import the data

    Return:
        a pandas DataFrame
    """
    tic = datetime.datetime.now()

    f = open(path, "r")
    ecm_results = json.load(f)
    f.close()

    ecm_results_keys  = list(ecm_results)
    ecm_results_keys.remove('On-site Generation')

    CMS = "Markets and Savings (by Category)"

    cms = [{
        'ecm' : ecm
        , 'adoption_scenario' : ap
        , 'variable' : v
        , 'region' : rg
        , 'building_class' : bg
        , 'end_use' : eu
        , 'fuel_type' : fl   # THIS MAY NOT ALWAYS EXIST
        , 'year'    : yr
        , 'value'   : value
        }\
            for ecm in ecm_results_keys\
            for ap  in list(ecm_results[ecm][CMS])\
            for v   in list(ecm_results[ecm][CMS][ap])\
            for rg  in list(ecm_results[ecm][CMS][ap][v])\
            for bg  in list(ecm_results[ecm][CMS][ap][v][rg])\
            for eu  in list(ecm_results[ecm][CMS][ap][v][rg][bg])\
            for fl  in list(ecm_results[ecm][CMS][ap][v][rg][bg][eu])\
            for yr  in list(ecm_results[ecm][CMS][ap][v][rg][bg][eu][fl])\
            for value in   [ecm_results[ecm][CMS][ap][v][rg][bg][eu][fl][yr]]
            ]

    cms = pd.DataFrame.from_dict(cms)

    cms["cms"] = CMS

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a Dataframe in {time_delta}")

    return cms

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

