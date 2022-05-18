from scout.utilities import json_to_df
from scout.utilities import isfloat

################################################################################
class ecm_results:                                                         # {{{
    def __init__(self, path): # {{{
        self.basename = os.path.basename(path)
        self.path = path
        self.df = json_to_df(path)
    # }}}

    def info(self): #{{{
        print(f"path:                           {self.path}")
        print(f"basename:                       {self.basename}")
    #}}}

#}}}



################################################################################
def import_ecm_results(path): # {{{
    df = json_to_df(path)
    assert any(df.lvl0 == "On-site Generation")

    # split the data set into several smaller data frames,
    # 1. On-site Generation
    # 2. ECMs
    #    a. Filter Variables
    #    b. Markets and Savings
    #    c.
    on_site_generation = df[df.lvl0 == "On-site Generation"]
    ecms               = df[df.lvl0 != "On-site Generation"]
    ecms = ecms.rename(columns = {"lvl0" : "ecm"})
    filter_variables   = ecms[ecms.lvl1 == "Filter Variables"]
    ecms               = ecms[ecms.lvl1 != "Filter Variables"]

    ############################################################################
    # clean up the on-site generation data frame
    assert all(on_site_generation.lvl7.isna())
    assert all(on_site_generation.lvl8.isna())
    assert all(on_site_generation.lvl9.isna())
    on_site_generation = on_site_generation.drop(columns = ["lvl0", "lvl7", "lvl8", "lvl9"])

    # verify that the "Overall" sums are equivalent to the sum over the regions
    # and building type
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl6"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"]
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl5"] = on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"]

    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl4"] = None
    on_site_generation.loc[on_site_generation.lvl2 == "Overall", "lvl3"] = None

    on_site_generation.lvl6 = on_site_generation.lvl6.apply(float)

    x = on_site_generation\
            .groupby(["lvl1", "lvl2", "lvl5"])\
            .agg({"lvl6" : "sum"})
    x.reset_index(inplace = True)
    x = x.pivot(index = ["lvl1", "lvl5"], columns = ["lvl2"], values = ["lvl6"])
    x.reset_index(inplace = True)
    x["abs_delta"] = abs(x.lvl6["By Category"] - x.lvl6["Overall"])

    #print(x[x.abs_delta > 1e-8])
    #assert all(x["abs_delta"] < 1e-8)
    if any(x.abs_delta < 1e-8):
        warnings.warn("At least one on_site_generation aggregation differs from 'Overall' value.")

    # only return the "by category" data as the "overall" is redundant
    on_site_generation = on_site_generation[on_site_generation.lvl2 == "By Category"]
    on_site_generation = on_site_generation.drop(columns = ["lvl2"])

    # rename columns in the on_site_generation frame for human ease of use
    on_site_generation.rename(columns = {
        "lvl1" : "metric",
        "lvl3" : "region",
        "lvl4" : "building_type",
        "lvl5" : "year",
        "lvl6" : "value"},
        inplace = True)

    # set data types
    assert all(on_site_generation.value.apply(isfloat))
    on_site_generation.value = on_site_generation.value.apply(float)

    assert all(on_site_generation.year.str.contains(r"^\d{4}$"))
    on_site_generation.year = on_site_generation.year.apply(int)

    ############################################################################
    # clean up filter_variables
    filter_variables = filter_variables.pivot(index = ["ecm"],
            columns = ["lvl2"],
            values  = ["lvl3"])

    filter_variables = filter_variables.reset_index(col_level = 1)
    filter_variables.columns = filter_variables.columns.map(lambda t: t[1])

    ############################################################################
    # markets_and_savings
    #
    # Ignore the Markets and Savings (Overall), no need to import aggregated
    # data
    ecm_mas = ecms[ecms.lvl1 == "Markets and Savings (by Category)"]
    ecm_mas = ecm_mas.drop(columns = ["lvl1"])
    ecm_mas = ecm_mas.rename(columns = {
        "lvl2" : "scenario",
        "lvl3" : "metric",
        "lvl4" : "region",
        "lvl5" : "building_class",
        "lvl6" : "end_use",
        "lvl7" : "fuel_type",
        "lvl8" : "year",
        "lvl9" : "value"
        })

    # verify assumption that all fuel_types are defined
    assert all(ecm_mas.fuel_type.notna())

    # move data from one column to another as needed
    idx = ecm_mas.fuel_type.str.contains("^\d{4}$")
    ecm_mas.loc[idx, "value"]     = ecm_mas.loc[idx, "year"]
    ecm_mas.loc[idx, "year"]      = ecm_mas.loc[idx, "fuel_type"]
    ecm_mas.loc[idx, "fuel_type"] = "Not Applicable"

    # set data types
    assert all(ecm_mas.value.apply(isfloat))
    ecm_mas.value = ecm_mas.value.apply(float)

    assert all(ecm_mas.year.str.contains("^\d{4}$"))
    ecm_mas.year = ecm_mas.year.apply(int)

    ############################################################################
    # financial_metrics
    financial_metrics = ecms[ecms.lvl1 == "Financial Metrics"]
    financial_metrics = financial_metrics[["ecm", "lvl2", "lvl3", "lvl4"]]
    financial_metrics = financial_metrics.rename(columns =
            {"lvl2" : "metric", "lvl3" : "year", "lvl4" : "value"})

    # set data types
    assert all(financial_metrics.value.apply(isfloat))
    financial_metrics.value = financial_metrics.value.apply(float)

    assert all(financial_metrics.year.str.contains("^\d{4}$"))
    financial_metrics.year = financial_metrics.year.apply(int)

    ############################################################################
    # return a tuple of data frames
    return ecm_mas, financial_metrics, filter_variables, on_site_generation

# }}}
