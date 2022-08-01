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
import os
from scout.utilities import json_to_df

################################################################################
# import data                                                              # {{{

# ECM results
ecm_result_paths = [
          "./Results_Files_3/ecm_results_1-1.json.gz"
        , "./Results_Files_3/ecm_results_2.json.gz"
        , "./Results_Files_3/ecm_results_3-1.json.gz"]

ecm_results =\
        pd.concat(
                [json_to_df(path = p) for p in ecm_result_paths]
                , keys = [os.path.basename(str(p)).split(".", 1)[0] for p in ecm_result_paths]
                )

# baseline values
baseline = json_to_df(path = "./supporting_data/stock_energy_tech_data/mseg_res_com_emm")

# conversion coefficients
conversion_coefficients = \
        json_to_df(path = './supporting_data/convert_data/emm_region_emissions_prices.json')

# }}}

################################################################################
# Define maps form one variable set to another                             # {{{

# needed conversation coefficients # {{{
conversion_coefficients = \
    conversion_coefficients[(conversion_coefficients.lvl0 == "CO2 intensity of electricity") &
                            (conversion_coefficients.lvl1 == "data")]

conversion_coefficients.drop(columns = ["lvl1", "lvl5"], inplace = True)
conversion_coefficients.rename(columns = {
      "lvl0" : "conversion"
    , "lvl2" : "region"
    , "lvl3" : "year"
    , "lvl4" : "value"
    },
    inplace = True)
# }}}

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

emf_end_uses =\
        pd.DataFrame(data = {
              "Cooking"                   : "Appliances"  # ecm_results
            , "Cooling (Env.)"            : np.nan        # ecm_results
            , "Cooling (Equip.)"          : "Cooling"     # ecm_results
            , "Computers and Electronics" : "Other"       # ecm_results
            , "Heating (Env.)"            : np.nan        # ecm_results
            , "Heating (Equip.)"          : "Heating"     # ecm_results
            , "Lighting"                  : "Lighting"    # ecm_results
            , "Other"                     : "Other"       # ecm_results
            , "Refrigeration"             : "Appliances"  # ecm_results
            , "Ventilation"               : np.nan        # ecm_results
            , "Water Heating"             : "Appliances"  # ecm_results
            , 'ceiling fan'               : "Appliances"  # baseline
            , "cooking"                   : "Appliances"  # baseline
            , 'cooling'                   : "Cooling"     # baseline
            , 'computers'                 : "Other"       # baseline
            , 'drying'                    : "Appliances"  # baseline
            , 'fans and pumps'            : "Heating"     # baseline
            , 'heating'                   : "Heating"     # baseline
            , 'lighting'                  : "Lighting"    # baseline
            , 'MELs'                      : "Other"       # baseline
            , 'non-PC office equipment'   : "Other"       # baseline
            , 'other'                     : "Other"       # baseline
            , 'onsite generation'         : np.nan        # baseline
            , 'PCs'                       : "Other"       # baseline
            , 'refrigeration'             : "Appliances"  # baseline
            , 'secondary heating'         : "Heating"     # baseline
            , 'TVs'                       : "Other"       # baseline
            , 'ventilation'               : "Heating"     # baseline
            , 'water heating'             : "Appliances"  # baseline
            }.items(),
            columns = ["scout_end_use", "emf_end_use"]
            )


emf_direct_indirect_fuel =\
        pd.DataFrame(data = {
            "Natural Gas"      : "Direct",
            "natural gas"      : "Direct",
            "Distillate/Other" : "Direct",
            "distillate"       : "Direct",
            "Biomass"          : "Direct",
            "Propane"          : "Direct",
            "Electric"         : "Indirect",
            "electricity"      : "Indirect",
            "Non-Electric"     : "Direct",
            "other fuel"       : "Direct"
            }.items(),
            columns = ["scout_fuel_type", "emf_direct_indirect_fuel"]
            )

emf_base_string =\
    pd.DataFrame(data = {
        "Avoided CO\u2082 Emissions (MMTons)" : "*Emissions|CO2|Energy|Demand|Buildings",
        "Energy Savings (MMBtu)"              : "*Final Energy|Buildings"
        }.items(),
        columns = ["impact", "emf_base_string"]
        )


# NOTE: Mapping to EMF fuel types _might_ require a mapping that uses both fuel
# type and end use.  In the example script the combination of fuel_type = "distillate" and
# end_use = "secondary heating (kerosene)" maps to "Oil_kerosene".
# 
# Other possible end uses that will need to be accounted for,
#   * stove (wood)
#   * secondary heater (wood)
emf_fuel_types =\
        pd.DataFrame(data = {
              "Natural Gas"      : "Gas"              # ecm_results
            , "natural gas"      : "Gas"              # baseline
            , "Propane"          : "Gas"
            , "Distillate/Other" : "Oil"
            , "distillate"       : "Oil"
            , "Biomass"          : "Biomass Solids"  # ecm_results
            , "other fuel"       : "Biomass Solids"  # baseline
            , "Electric"         : "Electricity"
            , "Electricity"      : "Electricity"
            , "electricity"      : "Electricity"       # baseline
            # , "???"              : "Oil_kerosene"      # baseline
            }.items(),
            columns = ["scout_fuel_type", "emf_fuel_type"]
            )

# }}}

################################################################################
# Collect the needed rows from ecm_results                                 # {{{
ecm_results = ecm_results.loc[ecm_results.lvl1 == "Markets and Savings (by Category)",:]
ecm_results.drop(columns = ["lvl1"], inplace = True)

#ecm_results.reset_index(inplace = True, drop = True)

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

# clean up
ecm_results.reset_index(inplace = True, drop = False)
ecm_results.rename(columns = {"level_0" : "file"}, inplace = True)
ecm_results.drop(columns = ["level_1"], inplace = True)

# some spot checks
ecm_results
set(ecm_results.ecm)
set(ecm_results.adoption_scenario)
set(ecm_results.impact)
set(ecm_results.region)
set(ecm_results.building_class_construction)
set(ecm_results.fuel_type)
set(ecm_results.year)

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

# }}}

################################################################################
# collect the needed rows form the baseline data                           # {{{

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
# ecm_results: unit and type conversions {{{

# set column types
ecm_results.value = ecm_results.value.apply(float)
ecm_results.year  = ecm_results.year.apply(int)

# Convert MMBtu to Exajoules
idx = ecm_results.impact.str.contains("MMBtu")
ecm_results.loc[idx, "value"] *= 1.05505585262e-9
ecm_results.impact = ecm_results.impact.str.replace("MMBtu", "EJ")
# }}}

################################################################################
# ecm_results aggregation {{{

a0 = ecm_results\
        .groupby(["file", "region", "emf_base_string", "year"])\
        .agg(value = ("value", "sum"))

a1 = ecm_results\
        .groupby(["file", "region", "emf_base_string", "building_class", "year"])\
        .agg(value = ("value", "sum"))

a2 = ecm_results\
        .groupby(["file", "region", "emf_base_string", "building_class", "emf_end_use", "year"])\
        .agg(value = ("value", "sum"))

a3_0 = ecm_results\
        [ecm_results.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "direct_indirect_fuel", "year"])\
        .agg(value = ("value", "sum"))
a3_1 = ecm_results\
        [ecm_results.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "building_class", "direct_indirect_fuel", "year"])\
        .agg(value = ("value", "sum"))
a3_2 = ecm_results\
        [ecm_results.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "building_class", "emf_end_use", "direct_indirect_fuel", "year"])\
        .agg(value = ("value", "sum"))

a4_0 = ecm_results\
        [ecm_results.emf_base_string == "*Final Energy|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "emf_fuel_type", "year"])\
        .agg(value = ("value", "sum"))
a4_1 = ecm_results\
        [ecm_results.emf_base_string == "*Final Energy|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "building_class", "emf_fuel_type", "year"])\
        .agg(value = ("value", "sum"))
a4_2 = ecm_results\
        [ecm_results.emf_base_string == "*Final Energy|Buildings"]\
        .groupby(["file", "region", "emf_base_string", "building_class", "emf_end_use", "emf_fuel_type", "year"])\
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
ecm_results_emf_aggregation = pd.concat([
    a0[["file", "emf_string", "year", "value"]],
    a1[["file", "emf_string", "year", "value"]],
    a2[["file", "emf_string", "year", "value"]],
    a3_0[["file", "emf_string", "year", "value"]],
    a3_1[["file", "emf_string", "year", "value"]],
    a3_2[["file", "emf_string", "year", "value"]],
    a4_0[["file", "emf_string", "year", "value"]],
    a4_1[["file", "emf_string", "year", "value"]],
    a4_2[["file", "emf_string", "year", "value"]]
    ])

# create a wide version of the ecm_results_emf_aggregation
ecm_results_emf_aggregation_wide = ecm_results_emf_aggregation.copy(deep = True)

ecm_results_emf_aggregation_wide.year =\
        ecm_results_emf_aggregation_wide.year.apply(str) # this is needed so the column names post pivot are strings

ecm_results_emf_aggregation_wide =\
        ecm_results_emf_aggregation_wide.pivot_table(
                index = ["file", "emf_string"],
                columns = ["year"],
                values = ["value"]
                )

ecm_results_emf_aggregation_wide.columns = ecm_results_emf_aggregation_wide.columns.droplevel(0)

ecm_results_emf_aggregation.reset_index(inplace = True, drop = True)
ecm_results_emf_aggregation_wide.reset_index(inplace = True, drop = False)

print(ecm_results_emf_aggregation)
print(ecm_results_emf_aggregation_wide)

# }}}







################################################################################
# Add emf_columns to baseline {{{

# emf_base_string for the baseline data is the same for all rows, Final Energy.
# Conversion to CO2 will occur after aggregation of the energy use

baseline["emf_base_string"] = "*Final Energy|Buildings"

baseline = baseline\
        .merge(
                building_type_to_class,
                how = "left",
                on = "building_type"
                )\
        .merge(
                emf_end_uses,
                how = "left",
                on = "end_use")\
        .merge(
                emf_fuel_types,
                how = "left",
                on = "fuel_type"
                )

baseline

# }}}

################################################################################
# unit conversions and structure
#
# after building out the aggregation for the values there was a lot of unit
# conversion taking place with a lot of logic to get the work done right.  I
# think it would be easier to build out the needed unit conversions first and
# then do the aggregations.
#
# To the best of my knowledge the units for the value column in the baseline
# DataFrame are in MMBtu
baseline.rename(columns = {"value" : "MMBtu"}, inplace = True)

# Unit conversions.
# The value column is in MMBtu and needs to be in EJ (extajuls)
MMBtu_to_EJ           = 1.05505585262e-9
EJ_to_quad            = 0.9478
pound_to_mt           = 0.000453592
EJ_to_twh             = 277.778
EJ_to_mt_co2_propane  = EJ_to_quad * 62.88
EJ_to_mt_co2_kerosene = EJ_to_quad * 73.38
EJ_to_mt_co2_gas      = EJ_to_quad * 53.056
EJ_to_mt_co2_oil      = EJ_to_quad * 74.14
EJ_to_mt_co2_bio      = EJ_to_quad * 96.88


# CROSS WALK
crosswalk =\
    pd.concat([
        ecm_results[["fuel_type", "end_use"]].drop_duplicates(),
        baseline[["fuel_type", "end_use"]].drop_duplicates()]
        ).reset_index(drop = True)

crosswalk.rename(columns = {
    "fuel_type" : "scout_fuel_type",
    "end_use"   : "scout_end_use"
    },
    inplace = True)

#
emf_direct_indirect_fuel


#{
#        "other fuel" : {
#              "secondary heater (LPG)" : EJ_to_mt_co2_propane,
#            , "furnace (LPG)" : EJ_to_mt_co2_propane
#            }
#        ,
#        "natural gas" : {
#              "water heating" : EJ_to_mt_co2_gas
#



        # "electricity" requires the conversion_coefficients data.frame


# create a EJ (extajuls) column
baseline["EJ"] = baseline.MMBtu * MMBtu_to_EJ

baseline

################################################################################
# Aggregation of energy use within baseline {{{

baseline.value = baseline.value.apply(float)
baseline.year  = baseline.year.apply(int)

# TODO: when are the supply_demand flags to be used?  Stock/energy flags?

b0 = baseline\
        .groupby(["region", "emf_base_string", "year"])\
        .agg(value = ("value", "sum"))

b1 = baseline\
        .groupby(["region", "emf_base_string", "emf_fuel_type", "year"])\
        .agg(value = ("value", "sum"))

b2 = baseline\
        .groupby(["region", "emf_base_string", "building_class", "emf_fuel_type", "year"])\
        .agg(value = ("value", "sum"))

b3 = baseline\
        .groupby(["region", "emf_base_string", "building_class", "end_use", "emf_fuel_type", "year"])\
        .agg(value = ("value", "sum"))

b0.reset_index(inplace = True)
b1.reset_index(inplace = True)
b2.reset_index(inplace = True)
b3.reset_index(inplace = True)

b0["emf_string"] = b0.region + b0.emf_base_string
b1["emf_string"] = b1.region + b1.emf_base_string + "|" + b1.emf_fuel_type
b2["emf_string"] = b2.region + b2.emf_base_string + "|" + b2.building_class + "|" + b2.emf_fuel_type
b3["emf_string"] = b3.region + b3.emf_base_string + "|" + b3.building_class + "|" + b3.end_use + "|" + b3.emf_fuel_type

baseline_emf_aggregation = pd.concat( [b0, b1, b2, b3])
baseline_emf_aggregation

# Unit conversions.
# The value column is in MMBtu and needs to be in EJ (extajuls)
MMBtu_to_EJ           = 1.05505585262e-9
EJ_to_quad            = 0.9478
pound_to_mt           = 0.000453592
EJ_to_twh             = 277.778
EJ_to_mt_co2_propane  = EJ_to_quad * 62.88
EJ_to_mt_co2_kerosene = EJ_to_quad * 73.38
EJ_to_mt_co2_gas      = EJ_to_quad * 53.056
EJ_to_mt_co2_oil      = EJ_to_quad * 74.14
EJ_to_mt_co2_bio      = EJ_to_quad * 96.88

# TODO: define coeffs_emm

baseline_emf_aggregation["EJ"] = baseline_emf_aggregation["value"] * MMBtu_to_EJ
baseline_emf_aggregation["CO2"] = np.nan # define the column for CO2

set(baseline_emf_aggregation.emf_string)

# TODO: rewrite as a for loop over a dict
baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Electricity"), "CO2"] =\
        baseline_emf_aggregation.EJ * coeffs_emm * EJ_to_twh

baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Gas_lpg"), "CO2"] =\
        baseline_emf_aggregation.EJ * EJ_to_mt_co2_propane

baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Gas"), "CO2"] =\
        baseline_emf_aggregation.EJ * EJ_to_mt_co2_gas

baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Oil_kerosene"), "CO2"] =\
        baseline_emf_aggregation.EJ * EJ_to_mt_co2_kerosene

baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Oil"), "CO2"] =\
        baseline_emf_aggregation.EJ * EJ_to_mt_co2_oil

baseline_emf_aggregation\
        .loc[baseline_emf_aggregation.emf_string.str.endswith("Biomass Solids"), "CO2"] =\
        baseline_emf_aggregation.EJ * EJ_to_mt_co2_bio


# }}}

################################################################################

################################################################################
#                                 End of file                                  #
################################################################################


