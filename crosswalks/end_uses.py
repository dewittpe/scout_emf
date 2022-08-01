import pandas as pd
import numpy as np
import itertools
pd.set_option('display.max_columns', None)

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

end_uses.to_csv("end_uses.csv", index = False)
