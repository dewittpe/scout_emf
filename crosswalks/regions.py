import pandas as pd
import numpy as np
import itertools

aia_climate_zones = ["AIA_CZ1", "AIA_CZ2", "AIA_CZ3", "AIA_CZ4", "AIA_CZ5"]
emm = ["TRE", "FRCC", "MISW", "MISC", "MISE", "MISS", "ISNE", "NYCW", "NYUP", "PJME", "PJMW", "PJMC", "PJMD", "SRCA", "SRSE", "SRCE", "SPPS", "SPPC", "SPPN", "SRSG", "CANO", "CASO", "NWPP", "RMRG", "BASN"]
states = ["AL", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

x = list(
    itertools.chain(
        [("AIA", r) for r in aia_climate_zones],
        [("EMM", r) for r in emm],
        [("States", r) for r in states]
        )
    )

scout_regions = pd.DataFrame(data = x, columns = ["region_set", "region"])

# define additional mappings
emm_to_avert =\
    pd.DataFrame(data =
        [("Northwest", "NWPP"),
         ("Great Basin", "BASN"),
         ("California", "CASO"),
         ("California", "CANO"),
         ("Rocky Mountains", "RMRG"),
         ("Upper Midwest", "SPPN"),
         ("Upper Midwest", "MISW"),
         ("Upper Midwest", "MISC"),
         ("Lower Midwest", "SPPC"),
         ("Lower Midwest", "SPPS"),
         ("Lakes/Mid-Atl.", "MISE"),
         ("Lakes/Mid-Atl.", "PJMW"),
         ("Lakes/Mid-Atl.", "PJMC"),
         ("Lakes/Mid-Atl.", "PJME"),
         ("Texas", "TRE"),
         ("Southwest", "SRSG"),
         ("Southeast", "PJMD"),
         ("Southeast", "SRCA"),
         ("Southeast", "SRSE"),
         ("Southeast", "FRCC"),
         ("Southeast", "MISS"),
         ("Southeast", "SRCE"),
         ("Northeast", "NYCW"),
         ("Northeast", "NYUP"),
         ("Northeast", "ISNE")],
        columns = ["avert_region", "EMM_region"]
        )

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
scout_regions.to_csv('regions.csv', index = False)

