import pandas as pd
import itertools

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

building.to_csv("building_type.csv", index = False)
