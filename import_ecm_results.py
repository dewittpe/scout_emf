import json
import pandas as pd
import re
import time
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

    if verbose:
        print(path + "\n  imported and coerced to a DataFrame in\n  " +\
                str(time.time() - tic) + " seconds.")

    return cms
