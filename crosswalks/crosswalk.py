import pandas as pd
import numpy as np
import itertools
pd.set_option('display.max_columns', None)




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

