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

        markets = []
        for i in range(len(data)):
            markets.append( json_to_df(data[i]["markets"]) )
            markets[i]["ecm"] = data[i]["name"]

        markets = pd.concat(markets)
        markets = markets.rename(columns = {"lvl0" : "scenario", "lvl1" : "mseg"})

        # split the data into several subsets
        self.lifetime_baseline = markets[(markets.lvl2 == "lifetime") & (markets.lvl3 == "baseline")]
        markets = markets[~((markets.lvl2 == "lifetime") & (markets.lvl3 == "baseline"))]

        self.lifetime_measure = markets[(markets.lvl2 == "lifetime") & (markets.lvl3 == "measure")]
        markets = markets[~((markets.lvl2 == "lifetime") & (markets.lvl3 == "measure"))]

        self.stock = markets[markets.lvl2 == "stock"]
        markets = markets[markets.lvl2 != "stock"]

        # clean up lifetime_baseline
        self.lifetime_baseline =\
                self.lifetime_baseline\
                .drop(columns = ["lvl2", "lvl3", "lvl6", "lvl7", "lvl8"])\
                .rename(columns = {"lvl4" : "year", "lvl5" : "value"})

        # clean up lifetime_measure
        self.lifetime_measure =\
                self.lifetime_measure\
                .drop(columns = ["lvl2", "lvl3", "lvl5", "lvl6", "lvl7", "lvl8"])\
                .rename(columns = {"lvl4" : "value"})

        # clean up stock
        self.stock = \
                self.stock\
                .drop(columns = ["lvl2", "lvl7", "lvl8"])\
                .rename(columns = {
                    "lvl3" : "total_or_competed",
                    "lvl4" : "measure_or_all",
                    "lvl5" : "year",
                    "lvl6" : "value"})

        # Clean up markets

        self.markets = markets
    # }}}

    def info(self): #{{{
        print(f"path:     {self.path}")
        print(f"basename: {self.basename}")
    #}}}

#}}}



################################################################################
#                                 End of File                                  #
################################################################################

