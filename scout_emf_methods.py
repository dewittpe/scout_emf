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
# * aggregate_emf
# * covert_energy_to_co2
#
################################################################################
import json
import pandas as pd
import re
import datetime

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
def import_baseline_energy_data(path, verbose = True):                      #{{{
    """ Import baseline energy data

    Arguments:
        path: file path to json file (mseg_res_com_emm_NEW.json)
        verbose: print time required to import the data
    """
    tic = datetime.datetime.now()

    f = open(path, "r")
    baseline = json.load(f)
    f.close()

    d = [{"ecm" : ecm, "bldg" : bd, "leaf": lf}\
            for ecm in list(baseline)\
            for bd  in list(baseline[ecm])\
            for lf  in     [baseline[ecm][bd]]
            ]

    # split the work into fuel and non-fuel dictionaries
    # to return a DataFrame of non-fuels use import_baseline_non_fuel_data
    fuels = []

    for i in range(len(d)):
        for l in list(d[i]["leaf"]):
            if l in ["electricity", "natural gas", "distillate", "other fuel"]:
                d1 = {"ecm" : d[i]["ecm"], "bldg" : d[i]["bldg"], "fuel" : l, "leaf" : d[i]["leaf"][l]}
                fuels.append(d1)

    # build a dictionary for fuels....
    # Well that mseg_res_com_emm_NEW.json has a unbelievable structure.  Divide
    # and conquer.
    fuels = [{"ecm" : fuels[i]["ecm"]
        , "bldg": fuels[i]["bldg"]
        , "fuel": fuels[i]["fuel"]
        , "enduse": eu
        , "leaf": leaf
        }\
                for i in range(len(fuels))\
                for eu in list(fuels[i]["leaf"])\
                for leaf in   [fuels[i]["leaf"][eu]]
                ]

    # Next, the leaf can have one of three general concepts for keys:
    # 1. stock/energy
    # 2. demand/supply
    # 3. appliances (including lightbulbs)
    fuels_2 = []

    for i in range(len(fuels)):
        for leaf in list(fuels[i]["leaf"]):
            d1 = {    "ecm"       : fuels[i]["ecm"]
                    , "bldg"      : fuels[i]["bldg"]
                    , "fuel"      : fuels[i]["fuel"]
                    , "enduse"    : fuels[i]["enduse"]
                    , "se"        : None
                    , "ds"        : None
                    , "appliance" : None
                    , "leaf"      : None
                    }
            if leaf in ["stock", "energy"]:
                d1["se"] = leaf
                d1["leaf"] = fuels[i]["leaf"][leaf]
            elif leaf in ["demand", "supply"]:
                d1["ds"] = leaf
                d1["leaf"] = fuels[i]["leaf"][leaf]
            else:
                d1["appliance"] = leaf
                d1["leaf"] = fuels[i]["leaf"][leaf]
            fuels_2.append(d1)

    # Next, the leafs could be one of three sets:
    # 1. year
    # 2. stock/energy
    # 3. appliance
    fuels_3 = []
    regex = re.compile(r"\d{4}")

    for i in range(len(fuels_2)):
        for leaf in list(fuels_2[i]["leaf"]):
            d1 = {    "ecm"       : fuels_2[i]["ecm"]
                    , "bldg"      : fuels_2[i]["bldg"]
                    , "fuel"      : fuels_2[i]["fuel"]
                    , "enduse"    : fuels_2[i]["enduse"]
                    , "se"        : fuels_2[i]["se"]
                    , "ds"        : fuels_2[i]["ds"]
                    , "appliance" : fuels_2[i]["appliance"]
                    , "year"      : None
                    , "leaf"      : None
                    , "value"     : None
                    }
            if leaf in ["stock", "energy"]:
                d1["se"] = leaf
                d1["leaf"] = fuels_2[i]["leaf"][leaf]
            elif regex.search(leaf):
                d1["year"] = leaf
                d1["value"] = fuels_2[i]["leaf"][leaf]
            elif leaf in ["N", "A"]:
                d1["value"] = None
            else:
                d1["appliance"] = leaf
                d1["leaf"] = fuels_2[i]["leaf"][leaf]
            fuels_3.append(d1)

    # Now, if the leaf is not None, then it could be year or energy/stock
    fuels_4 = []

    for i in range(len(fuels_3)):
        if fuels_3[i]["leaf"] is not None:
            d1 = {    "ecm"       : fuels_3[i]["ecm"]
                    , "bldg"      : fuels_3[i]["bldg"]
                    , "fuel"      : fuels_3[i]["fuel"]
                    , "enduse"    : fuels_3[i]["enduse"]
                    , "se"        : fuels_3[i]["se"]
                    , "ds"        : fuels_3[i]["ds"]
                    , "appliance" : fuels_3[i]["appliance"]
                    , "year"      : fuels_3[i]["year"]
                    , "leaf"      : fuels_3[i]["leaf"]
                    , "value"     : fuels_3[i]["value"]
                    }
            for leaf in list(fuels_3[i]["leaf"]):
                if leaf in ["stock", "energy"]:
                    d1["se"] = leaf
                    d1["leaf"] = fuels_3[i]["leaf"][leaf]
                elif leaf in ["N", "A"]:
                    d1["leaf"] = None
                else:
                    d1["year"] = leaf
                    d1["value"] = fuels_3[i]["leaf"][leaf]
                    d1["leaf"] = None
                fuels_4.append(d1)

    # finally, one more run though to get the yearly data
    fuels_5 = []

    for i in range(len(fuels_4)):
        if fuels_4[i]["leaf"] is not None:
            for leaf in list(fuels_4[i]["leaf"]):
                d1 = {    "ecm"       : fuels_4[i]["ecm"]
                        , "bldg"      : fuels_4[i]["bldg"]
                        , "fuel"      : fuels_4[i]["fuel"]
                        , "enduse"    : fuels_4[i]["enduse"]
                        , "se"        : fuels_4[i]["se"]
                        , "ds"        : fuels_4[i]["ds"]
                        , "appliance" : fuels_4[i]["appliance"]
                        , "year"      : fuels_4[i]["year"]
                        , "leaf"      : fuels_4[i]["leaf"]
                        , "value"     : fuels_4[i]["value"]
                        }
                if leaf in ["N", "A"]:
                    d1["leaf"] = None
                else:
                    d1["year"] = leaf
                    d1["value"] = fuels_4[i]["leaf"][leaf]
                    d1["leaf"] = None
                fuels_5.append(d1)

    rtn = pd.DataFrame.from_dict(fuels_5)
    rtn.drop(axis = 1, inplace = True, columns = "leaf")

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a DataFrame in {time_delta}")

    return rtn

# }}}

################################################################################
def import_baseline_building_data(path, verbose = True):                    #{{{
    """
    Arguments:
        path: file path to json file (mseg_res_com_emm_NEW.json)
        verbose: print time required to import the data
    """
    tic = datetime.datetime.now()

    f = open(path, "r")
    baseline = json.load(f)
    f.close()

    d = [{"ecm" : ecm, "bldg" : bd, "leaf": lf}\
            for ecm in list(baseline)\
            for bd  in list(baseline[ecm])\
            for lf  in     [baseline[ecm][bd]]
            ]

    # split the work into fuel and non-fuel dictionaries
    fuels = []
    non_fuels = []

    for i in range(len(d)):
        for l in list(d[i]["leaf"]):
            if l in ["electricity", "natural gas", "distillate", "other fuel"]:
                d1 = {"ecm" : d[i]["ecm"], "bldg" : d[i]["bldg"], "fuel" : l, "leaf" : d[i]["leaf"][l]}
                fuels.append(d1)
            else:
                d1 = {"ecm" : d[i]["ecm"], "bldg" : d[i]["bldg"], "variable" : l, "leaf" : d[i]["leaf"][l]}
                non_fuels.append(d1)

    # build a DataFrame for the non-fuels
    non_fuels = [{
                  "ecm"  : non_fuels[i]["ecm"]
                , "bldg" : non_fuels[i]["bldg"]
                , "variable" : non_fuels[i]["variable"]
                , "year" : yr
                , "value" : value
                }\
                        for i in range(len(non_fuels))\
                        for yr in list(non_fuels[i]["leaf"])\
                        for value in  [non_fuels[i]["leaf"][yr]]
                        ]

    non_fuels = pd.DataFrame.from_dict(non_fuels)

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a DataFrame in {time_delta}")

    return(non_fuels)

# }}}

################################################################################
def import_ecm_results(path                                                 #{{{
        , variables = ["Avoided CO\u2082 Emissions (MMTons)", "Energy Savings (MMBtu)"]
        , verbose = True):
    """ Import ECM results

    Arguments:
        path: file path to a ecm_results.json file
        variables: arrary of concepts to import, ignore others.
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
        , 'ftyv' : ftyv # this is a dictionary with possible fuel_type, year, and value
        }\
            for ecm in ecm_results_keys\
            for ap  in list(ecm_results[ecm][CMS])\
            for v   in list(ecm_results[ecm][CMS][ap]) if v in variables\
            for rg  in list(ecm_results[ecm][CMS][ap][v])\
            for bg  in list(ecm_results[ecm][CMS][ap][v][rg])\
            for eu  in list(ecm_results[ecm][CMS][ap][v][rg][bg])\
            for ftyv in   [ecm_results[ecm][CMS][ap][v][rg][bg][eu]]
            ]

    # if the fuel_type is not present, the keys will be years
    regex = re.compile(r"\d{4}")
    cms3 = []
    for i in range(len(cms)):
        k = list(cms[i]['ftyv'])
        if all([regex.search(k[j]) is not None for j in range(len(k))]):
            cms2 = [{
                  'ecm' : cms[i]["ecm"]
                , 'adoption_scenario' : cms[i]["adoption_scenario"]
                , 'variable' : cms[i]["variable"]
                , 'region' : cms[i]["region"]
                , 'building_class' : cms[i]["building_class"]
                , 'end_use' : cms[i]["end_use"]
                , 'fuel_type' : "Not applicable"
                , 'year' : yr
                , 'value' : value
                }\
                    for yr in list(cms[i]["ftyv"])\
                    for value in [cms[i]["ftyv"][yr]]
                    ]
        else:
            cms2 = [{
                  'ecm' : cms[i]["ecm"]
                , 'adoption_scenario' : cms[i]["adoption_scenario"]
                , 'variable' : cms[i]["variable"]
                , 'region' : cms[i]["region"]
                , 'building_class' : cms[i]["building_class"]
                , 'end_use' : cms[i]["end_use"]
                , 'fuel_type' : ft
                , 'year' : yr
                , 'value' : value
                }\
                    for ft in list(cms[i]["ftyv"])\
                    for yr in list(cms[i]["ftyv"][ft])\
                    for value in  [cms[i]["ftyv"][ft][yr]]
                    ]
        cms3.append(cms2)

    rtn = pd.concat([pd.DataFrame.from_dict(d) for d in cms3])
    rtn.reset_index(inplace = True, drop = True)

    if verbose:
        time_delta = datetime.datetime.now() - tic
        print(f"{path} imported and coerced to a DataFrame in {time_delta}")
        tic2 = datetime.datetime.now()
        print("Constructing additional columns now...")

    # Base EMF String -- only return the rows with a base sting
    idx = rtn.variable == "Avoided CO\u2082 Emissions (MMTons)"
    rtn.loc[idx, "emf_string"] = rtn.region[idx] + "*Emissions|CO2|Energy|Demand|Buildings"
    idx = rtn.variable == "Energy Savings (MMBtu)"
    rtn.loc[idx, "emf_string"] = rtn.region[idx] + "*Final Energy|Buildings"
    rtn = rtn[rtn.emf_string.notna()]

    # add helpful columns
    rtn["cms"] = CMS

    # residential or commercial?  split the existing building_class into two columns
    rtn.loc[rtn.building_class.isin(['Commercial (Existing)', 'Residential (Existing)']), "building_construction"] = "Existing"
    rtn.loc[rtn.building_class.isin(['Commercial (New)', 'Residential (New)']), "building_construction"] = "New"

    rtn.loc[rtn.building_class.isin(['Commercial (Existing)', 'Commercial (New)']), "building_class"] = "Commercial"
    rtn.loc[rtn.building_class.isin(['Residential (Existing)', 'Residential (New)']), "building_class"] = "Residential"

    # add column for direct fuel status.
    if not set(rtn.fuel_type).issubset(['Natural Gas', 'Distillate/Other', 'Biomass', 'Propane', 'Electric', 'Non-Electric']):
        # TODO: Improve error handling
        print("Unexpected fuel type")
        #exit(1)

    rtn.loc[rtn.fuel_type.isin(['Natural Gas', 'Distillate/Other', 'Biomass', 'Propane', 'Non-Electric']), "direct_fuel"] = "Direct"
    rtn.loc[rtn.fuel_type.isin(['Electric']), "direct_fuel"] = "Indirect"

    # fuel_type2
    rtn.loc[rtn.fuel_type.isin(['Natural Gas', 'Propane']), "fuel_type2"] = "Gas"
    rtn.loc[rtn.fuel_type.isin(['Distillate/Other']), "fuel_type2"] = "Oil"
    rtn.loc[rtn.fuel_type.isin(['Biomass']), "fuel_type2"] = "Biomass Solids"
    rtn.loc[rtn.fuel_type.isin(['Electric']), "fuel_type2"] =  "Electricity"

    # Simplified End use columns
    # TODO: Where should "Ventilation" be placed?
    # TODO: Where should "Heating (Env.)" and "Cooling (Env.)" be placed?

    rtn.loc[rtn.end_use.isin(['Cooking', 'Water Heating', 'Refrigeration']), "end_use2"] = "Appliances"
    rtn.loc[rtn.end_use.isin(['Cooling (Equip.)']), "end_use2"] = "Cooling"
    rtn.loc[rtn.end_use.isin(['Heating (Equip.)']), "end_use2"] = "Heating"
    rtn.loc[rtn.end_use.isin(['Lighting']), "end_use2"] =  "Lighting"
    rtn.loc[rtn.end_use.isin(['Computers and Electronics', "Other"]), "end_use2"] =  "Other"

    if verbose:
        time_delta = datetime.datetime.now() - tic2
        print(f"additional columns built in {time_delta}")

    return rtn

# }}}

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

