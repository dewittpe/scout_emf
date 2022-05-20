import os
import warnings
import numpy as np
import pandas as pd
from scout.utilities import json_to_df
from scout.utilities import isfloat


################################################################################
class ecm_results:                                                         # {{{
    def __init__(self, path): # {{{
        self.basename = os.path.basename(path)
        self.path = path

        df = json_to_df(path = path)

        # build individual DataFrames - start by splitting up the df
        osg  = df[df.lvl0 == "On-site Generation"]
        ecms = df[df.lvl0 != "On-site Generation"]

        # we can rename one of the columns for ecms
        ecms = ecms.rename(columns = {"lvl0" : "ecm"})

        # ecms will be split out further:
        financial_metrics  = ecms[ecms.lvl1 == "Financial Metrics"]
        filter_variables   = ecms[ecms.lvl1 == "Filter Variables"]
        mas                = ecms[((ecms.lvl1 != "Financial Metrics") & (ecms.lvl1 != "Filter Variables"))]

        # NOTE: additionally, the osg and mas will be split after some cleaning
        # steps into _by_category and _overall

        ########################################################################
        # clean up the on-site generation data frame
        assert all(osg.lvl7.isna())
        assert all(osg.lvl8.isna())
        assert all(osg.lvl9.isna())
        osg = osg.drop(columns = ["lvl0", "lvl7", "lvl8", "lvl9"])

        # The "Overall" version needs to have the year and value shifted over a
        # column
        osg.loc[osg.lvl2 == "Overall", "lvl6"] = osg.loc[osg.lvl2 == "Overall", "lvl4"]
        osg.loc[osg.lvl2 == "Overall", "lvl5"] = osg.loc[osg.lvl2 == "Overall", "lvl3"]

        osg.loc[osg.lvl2 == "Overall", "lvl4"] = np.nan
        osg.loc[osg.lvl2 == "Overall", "lvl3"] = np.nan

        # rename columns in the osg frame for human ease of use
        osg.rename(columns = {
            "lvl1" : "metric",
            # "lvl2" : "version" ---- "By Category" or "Overall"; will be dropped
            "lvl3" : "region",
            "lvl4" : "building_type",
            "lvl5" : "year",
            "lvl6" : "value"},
            inplace = True)

        # set data types
        assert all(osg.value.apply(isfloat))
        osg.value = osg.value.apply(float)

        assert all(osg.year.str.contains(r"^\d{4}$"))
        osg.year = osg.year.apply(int)

        self.osg_by_category = osg[osg.lvl2 == "By Category"].drop(columns = ["lvl2"])
        self.osg_overall     = osg[osg.lvl2 != "By Category"].drop(columns = ["lvl2", "region", "building_type"])

        ########################################################################
        # clean up filter_variables
        filter_variables = filter_variables.pivot(index = ["ecm"],
                columns = ["lvl2"],
                values  = ["lvl3"])

        filter_variables = filter_variables.reset_index(col_level = 1)
        filter_variables.columns = filter_variables.columns.map(lambda t: t[1])

        self.filter_variables = filter_variables

        ########################################################################
        # markets_and_savings
        #
        #mas = ecms[ecms.lvl1 == "Markets and Savings (by Category)"]
        #mas = mas.drop(columns = ["lvl1"])
        mas = mas.rename(columns = {
            # "lvl1" : "version", -- by Category or Overall; will be dropped
            "lvl2" : "scenario",
            "lvl3" : "metric",
            "lvl4" : "region",
            "lvl5" : "building_class",
            "lvl6" : "end_use",
            "lvl7" : "fuel_type",
            "lvl8" : "year",
            "lvl9" : "value"
            })

        # For the "Overall" set there are no region, building_class, end_use, or
        # fuel_type.  Move the values that are in the region and building_class
        # columns over to the year and value column respectivly
        idx = mas.lvl1 == "Markets and Savings (Overall)"
        assert all(mas[idx].value.isna())
        assert all(mas[idx].year.isna())
        assert all(mas[idx].fuel_type.isna())
        assert all(mas[idx].end_use.isna())

        mas.loc[idx, "value"] = mas.loc[idx, "building_class"]
        mas.loc[idx, "year"]  = mas.loc[idx, "region"]
        mas.loc[idx, "building_class"] = np.nan
        mas.loc[idx, "region"] = np.nan

        # move data from one column to another as needed, one place is when
        # fuel_type is not defined a year will be repored in that column
        idx = (mas.fuel_type.notna() & mas.fuel_type.str.contains(r"^\d{4}$"))
        mas.loc[idx, "value"]     = mas.loc[idx, "year"]
        mas.loc[idx, "year"]      = mas.loc[idx, "fuel_type"]
        mas.loc[idx, "fuel_type"] = np.nan

        # set data types
        assert all(mas.value.apply(isfloat))
        mas.value = mas.value.apply(float)

        assert all(mas.year.str.contains("^\d{4}$"))
        mas.year = mas.year.apply(int)

        self.mas_by_category = mas[mas.lvl1 == "Markets and Savings (by Category)"].drop(columns = ["lvl1"])
        self.mas_overall     = mas[mas.lvl1 == "Markets and Savings (Overall)"].drop(columns = ["lvl1", "region", "building_class", "end_use", "fuel_type"])

        ########################################################################
        # clean up financial_metrics
        financial_metrics = financial_metrics[["ecm", "lvl2", "lvl3", "lvl4"]]
        financial_metrics = financial_metrics.rename(columns =
                {"lvl2" : "metric", "lvl3" : "year", "lvl4" : "value"})

        # set data types
        assert all(financial_metrics.value.apply(isfloat))
        financial_metrics.value = financial_metrics.value.apply(float)

        assert all(financial_metrics.year.str.contains("^\d{4}$"))
        financial_metrics.year = financial_metrics.year.apply(int)

        self.financial_metrics = financial_metrics


    # }}}

    def by_category_vs_overall(self, tol = 1e-8): # {{{

        mas = self.mas_by_category\
                .groupby(["ecm", "scenario", "metric", "year"])\
                .agg({"value" : "sum"})\
                .reset_index()\
                .merge(self.mas_overall,
                        how = "outer",
                        on = ["ecm", "scenario", "metric", "year"],
                        suffixes = ("_aggregated", "_overall")
                        )
        mas["delta"] = mas.value_aggregated - mas.value_overall
        mas = mas[mas.delta > tol]

        osg = self.osg_by_category\
                .groupby(["metric", "year"])\
                .agg({"value" : "sum"})\
                .reset_index()\
                .merge(self.osg_overall,
                        how = "outer",
                        on = ["metric", "year"],
                        suffixes = ("_aggregated", "_overall")
                        )
        osg["delta"] = osg.value_aggregated - osg.value_overall
        osg = osg[osg.delta > tol]

        return {"Markets and Savings" : mas, "On-site Generation"  : osg}
    # }}}

    def info(self): #{{{
        print(f"path:     {self.path}")
        print(f"basename: {self.basename}")
        print("")
        print("Data Sets (all pandas DataFrames)")
        print("  * mas_by_category:    Markets and Savings (by Category)")
        print("  * mas_overall:        Markets and Savings (Overall)")
        print("  * financial_metrics:  Financial Metrics")
        print("  * filter_variables:   Filter Variables")
        print("  * osg_by_category:    On-site Generation (By Category)")
        print("  * osg_overall:        On-site Generation (Overall)")
        print("")
        print("Methods")
        print("  * by_category_vs_overall(tol = 1e-8):")
        print("      - returns DataFrames showing the differences between the 'By Category' and 'Overall' exceeding the tol(erance).")
    #}}}

#}}}



################################################################################
#                                 End of File                                  #
################################################################################

