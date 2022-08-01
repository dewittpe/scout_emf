import pandas as pd
import numpy as np
import itertools

# start with the ecm definition
end_uses = \
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


# ecm_definition, ecm_prep, ecm_results, emf



ecm_definition_to_emf =\
        pd.DataFrame(data = list([
            ( 'ceiling fan'               , "Other"   , "Other"   , "Appliances"),
            ( "cooking"                   , "Cooking" , "Cooking" , "Appliances"),
            ( 'cooling'                   ,                   "Cooling"   ),
            ( 'computers'                 ,                   "Other"     ),
            ( 'drying'                    ,                   "Appliances"),
            ( 'fans and pumps'            ,                   "Heating"   ),
            ( 'heating'                   ,                   "Heating"   ),
            ( 'lighting'                  ,                   "Lighting"  ),
            ( 'MELs'                      ,                   "Other"     ),
            ( 'non-PC office equipment'   ,                   "Other"     ),
            ( 'other'                     ,                   "Other"     ),
            ( 'onsite generation'         ,                   np.nan      ),
            ( 'PCs'                       ,                   "Other"     ),
            ( 'refrigeration'             ,                   "Appliances"),
            ( 'secondary heating'         ,                   "Heating"   ),
            ( 'TVs'                       ,                   "Other"     ),
            ( 'ventilation'               ,                   "Heating"   ),
            ( 'water heating'             ,                   "Appliances")
            ]),
            columns = ["ecm_definition_end_use", "ecm_prep_end_use", "ecm_results_end_use", "emf_end_use"]
            )

# define ecm_results to emf
ecm_results_to_emf =\
        pd.DataFrame(data = list([
            ( "Cooking"                   , "Appliances"),
            ( "Cooling (Env.)"            , np.nan      ),
            ( "Cooling (Equip.)"          , "Cooling"   ),
            ( "Computers and Electronics" , "Other"     ),
            ( "Heating (Env.)"            , np.nan      ),
            ( "Heating (Equip.)"          , "Heating"   ),
            ( "Lighting"                  , "Lighting"  ),
            ( "Other"                     , "Other"     ),
            ( "Refrigeration"             , "Appliances"),
            ( "Ventilation"               , np.nan      ),
            ( "Water Heating"             , "Appliances")
            ]),
            columns = ["ecm_results_end_use", "emf_end_use"]
            )


ecm_prep_to_emf




        self.out_break_enduses = OrderedDict([
            ('Heating (Equip.)', ["heating", "secondary heating"]),
            ('Cooling (Equip.)', ["cooling"]),
            ('Heating (Env.)', ["heating", "secondary heating"]),
            ('Cooling (Env.)', ["cooling"]),
            ('Ventilation', ["ventilation"]),
            ('Lighting', ["lighting"]),
            ('Water Heating', ["water heating"]),
            ('Refrigeration', ["refrigeration", "other"]),
            ('Cooking', ["cooking"]),
            ('Computers and Electronics', [
                "PCs", "non-PC office equipment", "TVs", "computers"]),
            ('Other', [
                "drying", "ceiling fan", "fans and pumps",
                "MELs", "other"])])




end_uses.to_csv("end_uses.csv", index = False)
