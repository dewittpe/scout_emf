import pandas as pd
import numpy as np
import itertools

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

technologies.to_csv("technologies.csv", index = False)
