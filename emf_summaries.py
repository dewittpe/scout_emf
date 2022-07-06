################################################################################
#
# Explicitly build out the emf_summaries here and then move them into a module
# format
#
# Will use some of the tools from the scout module dev work, like importing json
# to a pandas dataframe

################################################################################
import pandas as pd
import numpy as np
import warnings
from scout.utilities import json_to_df

################################################################################
# import ecm_results and baseline data                                     # {{{

# ecm_results = json_to_df(path = "./Results_Files_3/ecm_results_1-1.json.gz")
# ecm_results = json_to_df(path = "./Results_Files_3/ecm_results_2.json.gz")
ecm_results = json_to_df(path = "./Results_Files_3/ecm_results_3-1.json.gz")

baseline = json_to_df(path = "./supporting_data/stock_energy_tech_data/mseg_res_com_emm")
# }}}

################################################################################
# Define maps form one variable set to another                             # {{{
building_type_to_class =\
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

emf_end_uses =\
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

building_class_construction =\
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

emf_direct_indirect_fuel =\
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

emf_base_string =\
    pd.DataFrame(data = {
        "Avoided CO\u2082 Emissions (MMTons)" : "*Emissions|CO2|Energy|Demand|Buildings",
        "Energy Savings (MMBtu)"              : "*Final Energy|Buildings"
        }.items(),
        columns = ["impact", "emf_base_string"]
        )

emf_fuel_types =\
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

# }}}

################################################################################
# Collect the needed rows from ecm_results                                 # {{{
ecm_results = ecm_results.loc[ecm_results.lvl1 == "Markets and Savings (by Category)",:]
ecm_results.drop(columns = ["lvl1"], inplace = True)
ecm_results.reset_index(inplace = True, drop = True)

# rename columns
ecm_results.rename(
        columns = {
            "lvl0" : "ecm",
            "lvl2" : "adoption_scenario",
            "lvl3" : "impact",
            "lvl4" : "region",
            "lvl5" : "building_class_construction",
            "lvl6" : "end_use",
            "lvl7" : "fuel_type",
            "lvl8" : "year",
            "lvl9" : "value"
            },
        inplace = True)

# if fuel_type is missing then lvl9 will be empty
# move data over a colum and set a
idx = ecm_results.value.isna()
ecm_results.loc[idx, "value"] = ecm_results.loc[idx, "year"]
ecm_results.loc[idx, "year"]  = ecm_results.loc[idx, "fuel_type"]
ecm_results.loc[idx, "fuel_type"] = "Not Applicable (all fuels)"

# some spot checks
print(ecm_results))
print(set(ecm_results.ecm))
print(set(ecm_results.adoption_scenario))
print(set(ecm_results.impact))
print(set(ecm_results.region))
print(set(ecm_results.building_class_construction))
print(set(ecm_results.fuel_type))
print(set(ecm_results.year))

# }}}

################################################################################
# collect the needed rows form the base line data                          # {{{

# omit some rows with data on number of buildings
keep = ~baseline.lvl2.isin(["new homes", "total square footage",
    "new square footage", "total homes"])
baseline = baseline[keep]
baseline.reset_index(inplace = True, drop = True)

# remove useless rows
baseline = baseline[~((baseline.lvl6 == "stock") & (baseline.lvl7 == "NA")) ]
baseline = baseline[~((baseline.lvl5 == "stock") & (baseline.lvl6 == "NA")) ]
baseline = baseline[~((baseline.lvl4 == "stock") & (baseline.lvl5 == "NA")) ]

"""
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

# if stock/energy is in lvl4 then
baseline.loc[baseline.lvl4.isin(["stock", "energy"]),:]
baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl8"] = baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl6"]
baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl7"] = baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl5"]
baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl6"] = baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl4"]
baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl5"] = np.nan
baseline.loc[baseline.lvl4.isin(["stock", "energy"]), "lvl4"] = np.nan

# if stock/energy is in lvl5 then
baseline.loc[baseline.lvl5.isin(["stock", "energy"]),:]
baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl8"] =\
    baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl7"]
baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl7"] =\
    baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl6"]
baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl6"] =\
    baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl5"]
baseline.loc[baseline.lvl5.isin(["stock", "energy"]), "lvl5"] = np.nan

# when lvl4 is supply demand, and the above has been done, then lvl5 is all
# missing values and data can be shifted
baseline.loc[baseline.lvl4.isin(["supply", "demand"]),"lvl3"]
set(baseline.loc[~baseline.lvl4.isin(["supply", "demand"]),"lvl5"])

baseline.loc[~baseline.lvl4.isin(["supply", "demand"]),"lvl5"] = \
    baseline.loc[~baseline.lvl4.isin(["supply", "demand"]),"lvl4"]
baseline.loc[~baseline.lvl4.isin(["supply", "demand"]),"lvl4"] = np.nan

set(baseline.lvl0) # end use
set(baseline.lvl1) # end use
set(baseline.lvl2) # end use
set(baseline.lvl3) # end use
set(baseline.lvl3) # end use
set(baseline.lvl4) # supply/demand
set(baseline.lvl5) # technology_type
set(baseline.lvl6) # stock/energy
set(baseline.lvl7) # year

baseline.rename(
        columns = {
            "lvl0" : "region",
            "lvl1" : "building_type",
            "lvl2" : "fuel_type",
            "lvl3" : "end_use",
            "lvl4" : "supply_demand",
            "lvl5" : "technology_type",
            "lvl6" : "stock_energy",
            "lvl7" : "year",
            "lvl8" : "value"
            },
        inplace = True)

# }}}

################################################################################
# Add emf_columns to ecm_results {{{

ecm_results =\
    ecm_results\
    .merge(
            emf_base_string,
            how = "inner", # inner join so only the needed rows are retained
            on = "impact"
            )\
    .merge(
            building_class_construction,
            how = "left",
            left_on = "building_class_construction",
            right_on = "building_class0",
            suffixes = ("_x", "")
            )\
    .merge(
            emf_fuel_types,
            how = "left",
            on = "fuel_type"
            )\
    .merge(
            emf_direct_indirect_fuel,
            how = "left",
            on = "fuel_type"
            )\
    .merge(
            emf_end_uses,
            how = "left",
            on = "end_use"
            )

# report any unmapped fuels, end uses, ...
not_mapped = set(
        ecm_results.loc[
            (ecm_results.fuel_type.notna()) & (ecm_results.emf_fuel_type.isna())
            , "fuel_type"
            ])

if len(not_mapped):
    warnings.warn("ecm_results.fuel_type values not mapped to a emf_fuel_type value exist:\n" + ", ".join(not_mapped))


not_mapped = set(
        ecm_results.loc[
            (ecm_results.fuel_type.notna()) & (ecm_results.direct_indirect_fuel.isna())
            , "fuel_type"
            ])

if len(not_mapped):
    warnings.warn("ecm_results.fuel_type values not mapped to a direct/indirect value exist:\n" + ", ".join(not_mapped))

not_mapped = set(
        ecm_results.loc[
            (ecm_results.end_use.notna()) & (ecm_results.emf_end_use.isna())
            , "end_use"
            ])

if len(not_mapped):
    warnings.warn("ecm_results.end_use values not mapped to a emf_end_use value exist:\n" + ", ".join(not_mapped))
        
ecm_results.info()
emf_base_string

# }}}

################################################################################
# Add emf_columns to baseline {{{

# baseline  values are a mess and might require some additional logic, a simple
# merge isn't going to be sufficient at this moment. (at least for the
# emf_base_string)

baseline
emf_base_string

# }}}

################################################################################
#                                 End of file                                  #
################################################################################


