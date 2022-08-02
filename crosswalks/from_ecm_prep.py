        self.in_all_map = {
            "climate_zone": valid_regions,
            "bldg_type": {
                "residential": [
                    "single family home", "multi family home", "mobile home"],
                "commercial": [
                    "assembly", "education", "food sales", "food service",
                    "health care", "lodging", "large office", "small office",
                    "mercantile/service", "warehouse", "other"]},
            "structure_type": ["new", "existing"],
            "fuel_type": {
                "residential": [
                    "electricity", "natural gas", "distillate", "other fuel"],
                "commercial": [
                    "electricity", "natural gas", "distillate"]},
            "end_use": {
                "residential": {
                    "electricity": [
                        'drying', 'other', 'water heating',
                        'cooling', 'cooking', 'computers', 'lighting',
                        'secondary heating', 'TVs', 'heating', 'refrigeration',
                        'fans and pumps', 'ceiling fan'],
                    "natural gas": [
                        'drying', 'water heating', 'cooling', 'heating',
                        'cooking', 'secondary heating', 'other'],
                    "distillate": [
                        'water heating', 'heating', 'secondary heating',
                        'other'],
                    "other fuel": [
                        'water heating', 'cooking', 'heating',
                        'secondary heating', 'other']},
                "commercial": {
                    "electricity": [
                        'ventilation', 'water heating', 'cooling',
                        'heating', 'refrigeration', 'MELs',
                        'non-PC office equipment', 'PCs', 'lighting',
                        'cooking'],
                    "natural gas": [
                        'cooling', 'water heating', 'cooking', 'heating'],
                    "distillate": ['water heating', 'heating']}},
            "technology": {
                "residential": {
                    "supply": {
                        "electricity": {
                            'other': [
                                'dishwasher', 'clothes washing', 'freezers',
                                'rechargeables', 'coffee maker',
                                'dehumidifier', 'electric other',
                                'microwave', 'pool heaters and pumps',
                                'security system', 'portable electric spas',
                                'wine coolers'],
                            'water heating': ['solar WH', 'electric WH'],
                            'cooling': [
                                'room AC', 'ASHP', 'GSHP', 'central AC'],
                            'computers': [
                                'desktop PC', 'laptop PC', 'network equipment',
                                'monitors'],
                            'lighting': [
                                'linear fluorescent (T-8)',
                                'linear fluorescent (T-12)',
                                'reflector (LED)', 'general service (CFL)',
                                'external (high pressure sodium)',
                                'general service (incandescent)',
                                'external (CFL)',
                                'external (LED)', 'reflector (CFL)',
                                'reflector (incandescent)',
                                'general service (LED)',
                                'external (incandescent)',
                                'linear fluorescent (LED)',
                                'reflector (halogen)'],
                            'secondary heating': ['secondary heater'],
                            'TVs': [
                                'home theater and audio', 'set top box',
                                'video game consoles', 'DVD', 'TV'],
                            'heating': ['GSHP', 'resistance heat', 'ASHP'],
                            'ceiling fan': [None],
                            'fans and pumps': [None],
                            'refrigeration': [None],
                            'drying': [None],
                            'cooking': [None]},
                        "natural gas": {
                            'cooling': ['NGHP'],
                            'heating': ['furnace (NG)', 'NGHP', 'boiler (NG)'],
                            'secondary heating': ['secondary heater'],
                            'drying': [None],
                            'water heating': [None],
                            'cooking': [None],
                            'other': ["other appliances"]},
                        "distillate": {
                            'heating': [
                                'boiler (distillate)', 'furnace (distillate)'],
                            'secondary heating': ['secondary heater'],
                            'water heating': [None],
                            'other': ["other appliances"]},
                        "other fuel": {
                            'heating': [
                                'furnace (kerosene)',
                                'stove (wood)', 'furnace (LPG)'],
                            'secondary heating': [
                                'secondary heater (wood)',
                                'secondary heater (coal)',
                                'secondary heater (kerosene)',
                                'secondary heater (LPG)'],
                            'cooking': [None],
                            'water heating': [None],
                            'other': ["other appliances"]}},
                    "demand": [
                        'roof', 'ground', 'windows solar',
                        'windows conduction', 'equipment gain',
                        'people gain', 'wall', 'infiltration']},
                "commercial": {
                    "supply": {
                        "electricity": {
                            'ventilation': ['VAV_Vent', 'CAV_Vent'],
                            'water heating': [
                                'Solar water heater', 'HP water heater',
                                'elec_booster_water_heater',
                                'elec_water_heater'],
                            'cooling': [
                                'rooftop_AC', 'scroll_chiller',
                                'res_type_central_AC', 'reciprocating_chiller',
                                'comm_GSHP-cool', 'centrifugal_chiller',
                                'rooftop_ASHP-cool', 'wall-window_room_AC',
                                'screw_chiller'],
                            'heating': [
                                'electric_res-heat', 'comm_GSHP-heat',
                                'rooftop_ASHP-heat', 'elec_boiler'],
                            'refrigeration': [
                                'Commercial Beverage Merchandisers',
                                'Commercial Compressor Rack Systems',
                                'Commercial Condensers',
                                'Commercial Ice Machines',
                                'Commercial Reach-In Freezers',
                                'Commercial Reach-In Refrigerators',
                                'Commercial Refrigerated Vending Machines',
                                'Commercial Supermarket Display Cases',
                                'Commercial Walk-In Freezers',
                                'Commercial Walk-In Refrigerators'],
                            'MELs': [
                                'elevators', 'escalators', 'coffee brewers',
                                'kitchen ventilation', 'laundry',
                                'lab fridges and freezers', 'fume hoods',
                                'medical imaging', 'large video boards',
                                'shredders', 'private branch exchanges',
                                'voice-over-IP telecom', 'IT equipment',
                                'office UPS', 'data center UPS',
                                'security systems',
                                'distribution transformers',
                                'non-road electric vehicles'
                            ],
                            'lighting': [
                                '100W A19 Incandescent',
                                '100W Equivalent A19 Halogen',
                                '100W Equivalent CFL Bare Spiral',
                                '100W Equivalent LED A Lamp',
                                'Halogen Infrared Reflector (HIR) PAR38',
                                'Halogen PAR38',
                                'LED Integrated Luminaire',
                                'LED PAR38',
                                'Mercury Vapor',
                                'Metal Halide',
                                'Sodium Vapor',
                                'T5 4xF54 HO High Bay',
                                'T5 F28',
                                'T8 F28',
                                'T8 F32',
                                'T8 F59',
                                'T8 F96'
                            ],
                            'cooking': [
                                'electric_range_oven_24x24_griddle'],
                            'PCs': [None],
                            'non-PC office equipment': [None]},
                        "natural gas": {
                            'cooling': [
                                'gas_eng-driven_RTAC', 'gas_chiller',
                                'res_type_gasHP-cool',
                                'gas_eng-driven_RTHP-cool'],
                            'water heating': [
                                'gas_water_heater', 'gas_instantaneous_WH',
                                'gas_booster_WH'],
                            'cooking': [
                                'gas_range_oven_24x24_griddle'],
                            'heating': [
                                'gas_eng-driven_RTHP-heat',
                                'res_type_gasHP-heat', 'gas_boiler',
                                'gas_furnace']},
                        "distillate": {
                            'water heating': ['oil_water_heater'],
                            'heating': ['oil_boiler', 'oil_furnace']}},
                    "demand": [
                        'roof', 'ground', 'lighting gain',
                        'windows conduction', 'equipment gain',
                        'floor', 'infiltration', 'people gain',
                        'windows solar', 'ventilation',
                        'other heat gain', 'wall']}}}
