from scout.utilities import mapping_variables
from scout.utilities import json_to_df
from scout.utilities import isfloat
import pandas as pd
import numpy as np

################################################################################
def import_baseline(path): # {{{
    """
    Import Baseline data

    Per conversation with Chioke this is the outline of the structure of
    baseline json file
        lvl0: Region
        lvl1: building_type
        lvl2:
          one of two things:
          1. building type metadata
          2. fuel_type

        lvl3:
          if lvl2 is building type metadata then lvl3 the year (lvl4 value)
          if lvl2 is fuel type lvl3 is _always_ end_use

        lvl4:
          One of four things:
          1. values if lvl2 was building metadata
          2. if lvl2 is fuel type then
             a. supply/demand key if lvl3 is a heating or cooling end use
                (includes secondary heating)
             b. technology_type or
             c. stock/energy keys

        lvl5
          if (lvl4 = 2a) then technology_type / envelope components
          if (lvl4 = 2b) then stock/energy keys
          if (lvl4 = 2c) year or NA

        lvl6
          if (lvl4 = 2c) value
          if (lvl5 is stock/energy key) then NA or year
          if (lvl5 is technology_type / envelope components) then stock/energy
             key

        lvl7
          values or years

        lvl8
          values
    """

    maps = mapping_variables()#scout.utilities.maps()

    df = json_to_df(path = path)
    tdf = df.rename(columns = {"lvl0" : "region", "lvl1" : "building_type"})
    df = pd.merge(df, maps.building_type_to_class,
            how = "left",
            on = "building_type")

    assert all(df.building_class.notna())

    # split into two data frame
    bt_metadata = df[df.lvl5.isna()]
    df = df[df.lvl5.notna()]

    ############################################################################
    # clean up metadata
    bt_metadata = bt_metadata[["region", "building_type", "building_class", "lvl2", "lvl3", "lvl4"]]
    bt_metadata = bt_metadata.rename(columns =
            {"lvl2" : "impact", "lvl3" : "year", "lvl4" : "value"})

    assert all(bt_metadata.year.str.contains(r"^\d{4}$"))
    bt_metadata.year = bt_metadata.year.apply(int)

    assert all(bt_metadata.value.apply(isfloat))
    bt_metadata.value = bt_metadata.value.apply(float)

    ############################################################################
    # clean up df

    # remove useless rows
    df = df[~((df.lvl6 == "stock") & (df.lvl7 == "NA")) ]
    df = df[~((df.lvl5 == "stock") & (df.lvl6 == "NA")) ]
    df = df[~((df.lvl4 == "stock") & (df.lvl5 == "NA")) ]

    # move values from one column to the next.
    # * lvl8 will have all the "values" __ALL Exajoule__
    # * lvl7 will have all the years
    # * lvl6 will have all stock_energy indicators

    idx = (df.lvl4 == "stock") | (df.lvl4 == "energy")
    df.loc[idx, "lvl8"] = df.loc[idx, "lvl6"]
    df.loc[idx, "lvl7"] = df.loc[idx, "lvl5"]
    df.loc[idx, "lvl6"] = df.loc[idx, "lvl4"]
    df.loc[idx, "lvl5"] = np.nan
    df.loc[idx, "lvl4"] = np.nan

    idx = (df.lvl5 == "stock") | (df.lvl5 == "energy")
    df.loc[idx, "lvl8"] = df.loc[idx, "lvl7"]
    df.loc[idx, "lvl7"] = df.loc[idx, "lvl6"]
    df.loc[idx, "lvl6"] = df.loc[idx, "lvl5"]
    df.loc[idx, "lvl5"] = np.nan

    # if lvl4 is not demand/supply then it is a technology_type and needs to be
    # shifted over to lvl5
    idx = (df.lvl4.notna()) & (df.lvl4 != "demand") & (df.lvl4 != "supply")
    df.loc[idx, "lvl5"] = df.loc[idx, "lvl4"]
    df.loc[idx, "lvl4"] = np.nan

    # rename columns to be human useful
    df = df.rename(columns =
            {
                "lvl2" : "fuel_type",
                "lvl3" : "end_use",
                "lvl4" : "demand_supply",
                "lvl5" : "technology_type",
                "lvl6" : "stock_energy",
                "lvl7" : "year",
                "lvl8" : "Exajoules"
                })

    assert all(df.year.str.contains(r"^\d{4}$"))
    df.year = df.year.apply(int)

    assert all(df.Exajoules.apply(isfloat))
    df.Exajoules = df.Exajoules.apply(float)

    ############################################################################
    # return tuple of data frames
    return bt_metadata, df

# }}}
