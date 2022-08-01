import pandas as pd
import itertools

structure_type =\
        pd.DataFrame(data =
                list(itertools.chain(
                    [("Residential", bt) for bt in ["new", "existing"]],
                    [("Commercial", bt)  for bt in ["new", "existing"]]
                    ))
                , columns = ["building_class", "structure_type"]
                )

structure_type["ecm_prep_building"] =\
        structure_type.building_class +\
        " (" +\
        structure_type.structure_type.str.capitalize() +\
        ")"

structure_type.to_csv("structure_types.csv", index = False)
