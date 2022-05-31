import os
import warnings
import numpy as np
import pandas as pd
import json
import shutil
from scout.utilities import json_to_df
from scout.utilities import isfloat
from scout.utilities import mapping_variables

################################################################################
class ecm_prep:                                                            # {{{
    def __init__(self, path): # {{{
        self.basename = os.path.basename(path)
        self.path = path


        ########################################################################
        # import and format results
        f = open(path, "r")
        data = json.load(f)
        f.close()

        dfs = []
        for i in range(len(data)):
            dfs.append( scout.json_to_df(data[i]["markets"]) )
            dfs[i]["ecm"] = data[i]["name"]

        df = pd.concat(dfs)
        df = df.rename(columns =
                {"lvl0" : "scenario",
                 "lvl1" : "mseg"}
                )
        df


    # }}}

    def info(self): #{{{
        print(f"path:     {self.path}")
        print(f"basename: {self.basename}")
    #}}}

#}}}



################################################################################
#                                 End of File                                  #
################################################################################

