import json
import pandas as pd
import re
import time

def import_baseline(path, verbose = True):
    """ Import baseline data

    Arguments:
        path: file path to json file (mseg_res_com_emm_NEW.json)
        verbose: print time required to import the data
    """
    tic = time.time()

    f = open(path, "r")
    baseline = json.load(f)
    f.close()

    d = [{"ecm" : ecm, "bldg" : bd, "leaf": lf}\
            for ecm in list(baseline)\
            for bd  in list(baseline[ecm].keys())\
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
        d1 = {"ecm" : fuels[i]["ecm"]
                , "bldg" : fuels[i]["bldg"]
                , "fuel" : fuels[i]["fuel"]
                , "enduse" : fuels[i]["enduse"]
                , "se" : None
                , "ds" : None
                , "appliance" : None
                , "leaf" : None
                }
        for leaf in list(fuels[i]["leaf"]):
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

        for leaf in list(fuels_2[i]["leaf"]):
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

        if d1["leaf"] is not None:
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

    return(fuels_4)



    if verbose:
        print(path + "\n  imported and coerced to a DataFrame in\n  " +\
                str(time.time() - tic) + " seconds.")

    return rtn

def extract_non_fuel_baseline(d):
    """
    sub routine for import_baseline
    """





def import_ecm_results(path, verbose = True):
    """ Import ECM results

    Arguments:
        path: file path to a ecm_results.json file
        verbose : print time required to import the data

    Return:
        a pandas DataFrame
    """
    tic = time.time()

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
            for ap  in list(ecm_results[ecm][CMS].keys())\
            for v   in list(ecm_results[ecm][CMS][ap].keys())\
            for rg  in list(ecm_results[ecm][CMS][ap][v].keys())\
            for bg  in list(ecm_results[ecm][CMS][ap][v][rg].keys())\
            for eu  in list(ecm_results[ecm][CMS][ap][v][rg][bg].keys())\
            for ftyv in   [ecm_results[ecm][CMS][ap][v][rg][bg][eu]]
            ]

    # if the fuel_type is not present, the keys will be years
    regex = re.compile(r"\d{4}")
    cms3 = []
    for i in range(len(cms)):
        k = list(cms[i]['ftyv'].keys())
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
                    for yr in list(cms[i]["ftyv"].keys())\
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
                    for ft in list(cms[i]["ftyv"].keys())\
                    for yr in list(cms[i]["ftyv"][ft].keys())\
                    for value in  [cms[i]["ftyv"][ft][yr]]
                    ]
        cms3.append(cms2)

    rtn = pd.concat([pd.DataFrame.from_dict(d) for d in cms3])
    rtn.reset_index(inplace = True, drop = True)

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
        print(path + "\n  imported and coerced to a DataFrame in\n  " +\
                str(time.time() - tic) + " seconds.")

    return rtn

def import_ecm_results_v1(path, verbose = True):
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
    tic = time.time()

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
            for ap  in list(ecm_results[ecm][CMS].keys())\
            for v   in list(ecm_results[ecm][CMS][ap].keys())\
            for rg  in list(ecm_results[ecm][CMS][ap][v].keys())\
            for bg  in list(ecm_results[ecm][CMS][ap][v][rg].keys())\
            for eu  in list(ecm_results[ecm][CMS][ap][v][rg][bg].keys())\
            for fl  in list(ecm_results[ecm][CMS][ap][v][rg][bg][eu].keys())\
            for yr  in list(ecm_results[ecm][CMS][ap][v][rg][bg][eu][fl].keys())\
            for value in   [ecm_results[ecm][CMS][ap][v][rg][bg][eu][fl][yr]]
            ]

    cms = pd.DataFrame.from_dict(cms)

    cms["cms"] = CMS

    if verbose:
        print(path + "\n  imported and coerced to a DataFrame in\n  " +\
                str(time.time() - tic) + " seconds.")

    return cms


def aggregate_emf(df) :
    """ Aggregate results for EMF

    Arguments:
        df: a pandas DataFrame returned from import_ecm_results

    Return:
        a pandas DataFrame
    """
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

    return a


