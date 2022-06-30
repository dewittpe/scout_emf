import os
import warnings
import numpy as np
import pandas as pd
import json
import shutil
from scout.utilities import json_to_df
from scout.utilities import isfloat
from scout.utilities import mapping_variables

# SOME NOTES ON LEVELS FOR MARKETS
# under scenario
#
# under master_mseg there will be a different structure than mseg_out_break
#
# master_mseg are "totals"
#
# mseg_out_break are disaggregated by climiate zone, building type, end use,
# etc.
#
# lvl2 == metrics/parameters/impact
#
# lvl2 = energy and carbon have same structure
#
# lvl2 = cost ---->>>> cost + lvl3 value define the "cost"
#    lvl3 = stock  === capital
#    lvl3 = energy === utility bill
#    lvl3 = carbon === social cost
#
#
#


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

        self.master_mseg      = markets[(markets.mseg == "master_mseg") & (markets.lvl2 != "cost")]
        self.master_mseg_cost = markets[(markets.mseg == "master_mseg") & (markets.lvl2 == "cost")]

        self.mseg_out_break = markets[markets.mseg == "mseg_out_break"]

        # clean up lifetime_baseline
        self.lifetime_baseline =\
                self.lifetime_baseline\
                .drop(columns = ["lvl2", "lvl3", "lvl6", "lvl7", "lvl8", "lvl9"])\
                .rename(columns = {"lvl4" : "year", "lvl5" : "value"})
        self.lifetime_baseline.reset_index(drop = True, inplace = True)

        # clean up lifetime_measure
        self.lifetime_measure =\
                self.lifetime_measure\
                .drop(columns = ["lvl2", "lvl3", "lvl5", "lvl6", "lvl7", "lvl8", "lvl9"])\
                .rename(columns = {"lvl4" : "value"})
        self.lifetime_measure.reset_index(drop = True, inplace = True)

        # clean up stock
        self.stock = \
                self.stock\
                .drop(columns = ["lvl2", "lvl7", "lvl8", "lvl9"])\
                .rename(columns = {
                    "lvl3" : "total_or_competed",
                    "lvl4" : "measure_or_all",
                    "lvl5" : "year",
                    "lvl6" : "value"})
        self.stock.reset_index(drop = True, inplace = True)

        # Clean up markets

        self.master_mseg = \
                self.master_mseg\
                .drop(columns = ["mseg", "lvl7", "lvl8", "lvl9"])\
                .rename(columns = {
                    "lvl3" : "total_or_competed",
                    "lvl5" : "year",
                    "lvl6" : "value"})
        self.master_mseg.reset_index(drop = True, inplace = True)


        self.master_mseg_cost = \
                self.master_mseg_cost\
                .drop(columns = ["mseg", "lvl2", "lvl8", "lvl9"])\
                .rename(columns = {
                    "lvl4" : "total_or_competed",
                    "lvl6" : "year",
                    "lvl7" : "value"})
        self.master_mseg_cost.reset_index(drop = True, inplace = True)

        self.mseg_out_break = \
                self.mseg_out_break\
                .drop(columns = ["mseg"])\
                .rename(columns = {
                    "lvl2" : "impact",
                    "lvl3" : "lvl3",
                    "lvl4" : "region",
                    "lvl5" : "building_class",
                    "lvl6" : "end_use",
                    "lvl7" : "fuel_type",
                    "lvl8" : "year",
                    "lvl9" : "value"})
        self.mseg_out_break.reset_index(drop = True, inplace = True)

    # }}}

    def info(self): #{{{
        print(f"path:     {self.path}")
        print(f"basename: {self.basename}")
    #}}}

#}}}



################################################################################
#                                 End of File                                  #
################################################################################

