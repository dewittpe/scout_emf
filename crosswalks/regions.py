import pandas as pd
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

scout_regions.to_csv('regions.csv', index = False)

