import pandas as pd
import numpy as np
import itertools
pd.set_option('display.max_columns', None)


# Define the following objects
#
# scout_regions: a pandas DataFrame with two columns, ["region_set", "region"].
#   "region_set" denotes either
#     1. the American Institute of Architects (AIA) climate zones for the
#     contiguous United States, Alaska, and Hawaii
#     2. EIA Electricity Market Module (EMM) region
#     3. Contiguous U.S. states
#   The "region" are the specific values for the "region_set".
#
# scout_building_type

################################################################################
# Scout Regions {{{
aia_climate_zones = ["AIA_CZ1", "AIA_CZ2", "AIA_CZ3", "AIA_CZ4", "AIA_CZ5"]
emm = ["TRE", "FRCC", "MISW", "MISC", "MISE", "MISS", "ISNE", "NYCW", "NYUP", "PJME", "PJMW", "PJMC", "PJMD", "SRCA", "SRSE", "SRCE", "SPPS", "SPPC", "SPPN", "SRSG", "CANO", "CASO", "NWPP", "RMRG", "BASN"]
states = ["AL", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

x = list(
    itertools.chain(
        [("AIA", r) for r in aia_climate_zones],
        [("EMM", r) for r in emm],
        [("States", r) for r in states]
        )
    )

scout_regions = pd.DataFrame(data = x, columns = ["region_set", "region"])
scout_regions.to_csv('regions.csv')

# }}}

################################################################################
# scout building type {{{
res = [
"single family home", "multi family home", "mobile home"]

com = ["assembly", "education", "food sales", "food service", "health care", "lodging",
        "large office", "small office", "mercantile/service", "warehouse",
        "other"]

building =\
        pd.DataFrame(data = 
                list(itertools.chain(
                    [("Residential", bt) for bt in res],
                    [("Commercial", bt) for bt in com]
                    ))
                , columns = ["building_class", "building_type"]
)

structure_type =\
        pd.DataFrame(data = 
                list(itertools.chain(
                    [("Residential", bt) for bt in ["new", "existing"]],
                    [("Commercial", bt)  for bt in ["new", "existing"]]
                    ))
                , columns = ["building_class", "structure_type"]
                )

structure_type["ecm_prep_building"] = structure_type.building_class + " (" + structure_type.structure_type.str.capitalize() + ")" 
structure_type

pd.merge(building, structure_type, on = ["building_class"], how = "outer").to_csv("buildings.csv")


fuel_type =\
        pd.DataFrame(data = 
                list(itertools.chain(
                    [("Residential", bt) for bt in ["electricity", "natural gas", "distillate", "other fuel"]],
                    [("Commercial", bt)  for bt in ["electricity", "natural gas", "distillate"]]
                    ))
                , columns = ["building_class", "ecm_definition_fuel_type"]
                )

end_use = \
        pd.DataFrame(data =
                list(itertools.chain(
                    [("Residential", ft, "heating")           for ft in ["electricity", "natural gas", "distillate", "other fuel"]],
                    [("Residential", ft, "secondary heating") for ft in ["electricity", "natural gas", "distillate", "other fuel"]],
                    [("Residential", ft, "cooling")           for ft in ["electricity", "natural gas"                            ]],
                    [("Residential", ft, "water heating")     for ft in ["electricity", "natural gas", "distillate", "other fuel"]],
                    [("Residential", ft, "cooking")           for ft in ["electricity", "natural gas",               "other fuel"]],
                    [("Residential", ft, "drying")            for ft in ["electricity", "natural gas",               "other fuel"]],
                    [("Residential", "electricity", eu)       for eu in ["lighting", "refrigeration", "ceiling fan", "fans and pumps", "computers", "TVs"]],
                    [("Residential", ft, "other")             for ft in ["electricity", "natural gas", "distillate", "other fuel"]],

                    [("Commercial", ft, "heating")           for ft in ["electricity", "natural gas", "distillate"]],
                    [("Commercial", ft, "cooling")           for ft in ["electricity", "natural gas"              ]],
                    [("Commercial", ft, "water heating")     for ft in ["electricity", "natural gas", "distillate"]],
                    [("Commercial", ft, "cooking")           for ft in ["electricity", "natural gas",             ]],
                    [("Commercial", "electricity", eu)       for eu in ["ventilation", "lighting", "refrigeration", "PCs", "non-PC office equipment", "MELs"]],
                    ))
                , columns = ["building_class", "ecm_definition_fuel_type", "ecm_definition_end_use"]
                )

technology = \
        pd.DataFrame(data = list(itertools.chain(

              [("Residential", "Supply", "heating", "electricity", tech) for tech in ["AHSP", "GSHP", "resistance heat"]]
            , [("Residential", "Supply", "heating", "natural gas", tech) for tech in ["NGHP", "boiler (NG)", "furnace (NG)"]]
            , [("Residential", "Supply", "heating", "distillate",  tech) for tech in ["boiler (distillate)", "furnace (distillate)"]]
            , [("Residential", "Supply", "heating", "other fuel",  tech) for tech in ["furnace (LPG)", "furnace (kerosene)", "stove (wood)"]]

            , [("Residential", "Supply", "secondary heating", "electricity", "secondary heater")]
            , [("Residential", "Supply", "secondary heating", "natural gas", "secondary heater")]
            , [("Residential", "Supply", "secondary heating", "distillate",  "secondary heater")]
            , [("Residential", "Supply", "secondary heating", "other fuel",  "secondary heater (" + tech + ")") for tech in ["wood", "coal", "kerosene", "LPG"]]

            , [("Residential", "Supply", "cooling", "electricity", tech) for tech in ["room AC", "ASHP", "GSHP", "central AC"]]
            , [("Residential", "Supply", "cooling", "natural gas", tech) for tech in ["NGHP"]]

            , [("Residential", "Supply", "water heating", "electricity", tech) for tech in ["electric WH", "solar WH"]]
            , [("Residential", "Supply", "water heating", "natural gas", np.nan)]
            , [("Residential", "Supply", "water heating", "distillate",  np.nan)]
            , [("Residential", "Supply", "water heating", "other fuel",  np.nan)]

            , [("Residential", "Supply", "cooking", ft, np.nan) for ft in ["electricity", "natural gas", "other fuel"]] # all fuel types for cooking have a Null technology
            , [("Residential", "Supply", "drying", ft, np.nan) for ft in ["electricity", "natural gas", "other fuel"]]  # all fuel types for drying have a Null technology

            , [("Residential", "Supply", "lighting", "electricity", tech) for tech in ["general service (incandescent)", "general service (CFL)", "general service (LED)",
                                                                                       "relector (incandescent)", "reflector (halogen)", "reflector (CFL)", "reflector (LED)",
                                                                                       "linear flourescent (T-8)", "linear flourescent (T-12)", "linear flourescent (LED)",
                                                                                       "external (incandescent)", "external (high pressure sodium)", "external (CFL)", "external (LED)"]]

            , [("Residential", "Supply", "refrigeration", "electricity", np.nan)]
            , [("Residential", "Supply", "ceiling fan", "electricity", np.nan)]
            , [("Residential", "Supply", "fans and pumps", "electricity", np.nan)]

            , [("Residential", "Supply", "computers", "electricity", tech) for tech in ["desktop PC", "laptop PC", "network equipment", "monitors"]]
            , [("Residential", "Supply", "TVs", "electricity", tech) for tech in ["home theater and audio", "set top box", "video game consoles", "DVD", "TV"]]

            , [("Residential", "Supply", "other", "electricity", tech) for tech in ["dishwasher", "clothes washing", "freezers", "rechargebles", "coffee maker", "dehumidifier", "electric other", "microwave", "pool heaters and pumps", "security system", "portable electric spas", "wine coolers"]]
            , [("Residential", "Supply", "other", "natural gas", tech) for tech in ["other appliances"]]
            , [("Residential", "Supply", "other", "distillate", tech) for tech in ["other appliances"]]
            , [("Residential", "Supply", "other", "ohter fuel", tech) for tech in ["other appliances"]]

            , [("Residential", "Demand", np.nan, np.nan, tech) for tech in ["roof", "wall", "infiltration", "ground", "windows solar", "windows conduction", "equipment gain", "people gain"]]

            , [("Commercial", "Supply", "heating", "electricity", tech) for tech in ["electric_res-heat", "comm_GSHP-heat", "rooftop_ASHP-heat", "elec_boiler"]]
            , [("Commercial", "Supply", "heating", "natural gas", tech) for tech in ["gas_eng-driven_RTHP-heat", "res_type_gasHP-heat", "gas_boiler", "gas_furnace"]]
            , [("Commercial", "Supply", "heating", "distillate", tech) for tech in ["oil_boiler", "oil_furnace"]]
            
            , [("Commercial", "Supply", "cooling", "electricity", tech) for tech in ["roottop_AC", "scrool_chiller", "res_type_centeral_AC", "reciprocating_chiller", "comm_GSHP-cool", "centrigual_chiller", "rooftop_ASHP-cool", "wall-window_room_AC", "screw_chiller"]]
            , [("Commercial", "Supply", "cooling", "natural gas", tech) for tech in ["gas_eng-driven_RTAC", "gas_chiler", "res_type_gasHP-cool", "gas_eng-driven_RTHP-cool"]]
             
            , [("Commercial", "Supply", "ventilation", "electricity", tech) for tech in ["CAV_Vent", "VAV_Vent"]]
            
            , [("Commercial", "Supply", "water heating", "electricity", tech) for tech in ["Solar water heater", "HP water heater", "elec_booster_water_heater", "elec_water_heater"]]
            , [("Commercial", "Supply", "water heating", "natural gas", tech) for tech in ["gas_water_heater", "gas_instantaneous_WH", "gas_booster_WH"]]
            , [("Commercial", "Supply", "water heating", "distillate",  tech) for tech in ["oil_water_heater"]]

            , [("Commercial", "Supply", "lighting", "electricity", tech) for tech in ["100W A19 Incandescent", "100W Equivalent A19 Halogen", "100W Equivalent CFL Bare Spiral", "100W Equivalent LED A Lamp", "Halogen Infrared Reflector (HIR) PAR38", " Halogen PAR38", " LED PAR38", "T5 F28", " T8 F28", " T8 F32", " T8 F59", " T8 F96", "T5 4xF54 HO High Bay", " Mercury Vapor", " Metal Halide", " Sodium Vapor", "LED Integrated Luminaire"]]

            , [("Commercial", "Supply", "refrigeration", "electricity", tech) for tech in ["Commercial Beverage Merchandisers", " Commercial Compressor Rack Systems", " Commercial Condensers", " Commercial Ice Machines", " Commercial Reach-In Freezers", " Commercial Reach-In Refrigerators", " Commercial Refrigerated Vending Machines", " Commercial Supermarket Display Cases", " Commercial Walk-In Freezers", " Commercial Walk-In Refrigerators"]]

            , [("Commercial", "Supply", "cooking", "electricity", tech) for tech in ["electric_range_oven_24x24_griddle"]]
            , [("Commercial", "Supply", "cooking", "natural gas", tech) for tech in ["gas_range_oven_24x24_griddle"]]

            , [("Commercial", "Supply", "PCs", "electricity", np.nan)]
            , [("Commercial", "Supply", "non-PC office equipment", "electricity", np.nan)]

            , [("Commercial", "Supply", "MELs", "electricity", tech) for tech in ["elevators", " escalators", " coffee brewers", " kitchen ventilation", " laundry", " lab fridges and freezers", " fume hoods", " medical imaging", " large video boards", " shredders", " private branch exchanges", " voice-over-IP telecom", " IT equipment", " office UPS", " data center UPS", " security systems", " distribution transformers", " non-road electric vehicles"]]

            , [("Commercial", "Demand", np.nan, np.nan, tech) for tech in ["roof", "wall", "ground", "floor", "infiltration", "ventilation", "windows conduction", "windows solar", "lighting gain", "equipment gain", "people gain", "other heat gain"]]

            ))
            , columns = ["building_class", "ecm_definition_supply_demand", "ecm_definition_end_use", "ecm_definition_fuel_type", "ecm_definition_technology"]
            )



end_use

ecm_definition_to_scout_end_use =\
        pd.DataFrame(data = list(itertools.chain(
              [("heating", "Heating (Env.)", np.nan)]
            , [("heating", "Heating (Equip.)", "Heating")]
            ))
            , columns = ["ecm_definition_end_use", "ecm_results_end_use", "emf_end_use"])




scout_to_emf_end_use =\
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

scout_to_emf_direct_indirect_fuel =\
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
scout_to_emf_fuel_types =\
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
            }.items(),
            columns = ["scout_fuel_type", "emf_fuel_type"]
            )



crosswalk = pd.merge(fuel_type, end_use, on = ["building_class", "ecm_definition_fuel_type"], how = "outer")
crosswalk = pd.merge(crosswalk, technology, on = ["building_class", "ecm_definition_end_use", "ecm_definition_fuel_type"], how = "outer")

crosswalk = pd.merge(crosswalk, scout_to_emf_fuel_types, left_on = ["ecm_definition_fuel_type
scout_to_emf_fuel_types


print(crosswalk.head())
crosswalk.to_csv("crosswalk_wip.csv")

################################################################################
#                                 End of File                                  #
################################################################################

