import pandas as pd
import itertools

fuel_types =\
        pd.DataFrame(data =
                list(itertools.chain(
                    [("Residential", bt) for bt in ["electricity", "natural gas", "distillate", "other fuel"]],
                    [("Commercial", bt)  for bt in ["electricity", "natural gas", "distillate"]]
                    ))
                , columns = ["building_class", "ecm_definition_fuel_type"]
                )

fuel_types.to_csv("fuel_types.csv", index = False)
