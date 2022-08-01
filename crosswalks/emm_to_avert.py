import pandas as pd

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

emm_to_avert.to_csv("emm_to_avert.csv", index = False)

