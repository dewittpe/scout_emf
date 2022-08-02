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

out_break =\
        pd.DataFrame(data = [
            ("Single Family Homes"  , "single family home") , 
            ("Single Family Homes"  , "mobile home")        , 
            ("Multi Family Homes"   , "multi family home")  , 
            ("Hospitals"            , "health care")        , 
            ("Large Offices"        , "large office")       , 
            ("Small/Medium Offices" , "small office")       , 
            ("Retail"               , "food sales")         , 
            ("Retail"               , "mercantile/service") , 
            ("Hospitality"          , "lodging")            , 
            ("Hospitality"          , "food service")       , 
            ("Education"            , "education")          , 
            ("Assembly/Other"       , "assembly")           , 
            ("Assembly/Other"       , "other")              , 
            ("Warehouse"            , "warehouse")
            ],
            columns = ["out_break_building_type", "building_type"]
            )


building = pd.merge(building, out_break, on = "building_type")

building.to_csv("building_type.csv", index = False)
