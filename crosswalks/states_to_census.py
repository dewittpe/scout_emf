import pandas as pd
import itertools

# State to Census Region
state_to_census_region =\
        pd.DataFrame(data = itertools.chain(
    [("New England", s) for s in ['CT', 'MA', 'ME', 'NH', 'RI', 'VT']],
    [("Mid Atlantic", s) for s in ['NJ', 'NY', 'PA']],
    [("East North Central", s) for s in ['IL', 'IN', 'MI', 'OH', 'WI']],
    [("West North Central", s) for s in ['IA', 'KS', 'MN', 'MO', 'ND', 'NE', 'SD']],
    [("South Atlantic", s) for s in ['DC', 'DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV']],
    [("East South Central", s) for s in ['AL', 'KY', 'MS', 'TN']],
    [("West South Central", s) for s in ['AR', 'LA', 'OK', 'TX']],
    [("Mountain", s) for s in ['AZ', 'CO', 'ID', 'MT', 'NM', 'NV', 'UT', 'WY']],
    [("Pacific", s) for s in ['AK', 'CA', 'HI', 'OR', 'WA']]),
    columns = ["census_region", "state"]
)

# export results
state_to_census_region.to_csv('states_to_census_region.csv', index = False)

