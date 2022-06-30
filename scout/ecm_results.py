import os
import warnings
import numpy as np
import pandas as pd
import plotly.express as px
import shutil
from scout.utilities import json_to_df
from scout.utilities import isfloat
from scout.utilities import mapping_variables

################################################################################
class ecm_results:                                                         # {{{
    def __init__(self, path): # {{{
        self.basename = os.path.basename(path)
        self.path = path

        self.emf_aggregation = None
        self.by_category_aggreation_vs_overall = None

        ########################################################################
        # import and format results
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
        # clean up the on-site generation data frame # {{{
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
            "lvl1" : "impact",
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
        # }}}

        ########################################################################
        # clean up filter_variables # {{{
        filter_variables = filter_variables.pivot(index = ["ecm"],
                columns = ["lvl2"],
                values  = ["lvl3"])

        filter_variables = filter_variables.reset_index(col_level = 1)
        filter_variables.columns = filter_variables.columns.map(lambda t: t[1])

        self.filter_variables = filter_variables
        # }}}

        ########################################################################
        # markets_and_savings # {{{
        #
        #mas = ecms[ecms.lvl1 == "Markets and Savings (by Category)"]
        #mas = mas.drop(columns = ["lvl1"])
        mas = mas.rename(columns = {
            # "lvl1" : "version", -- by Category or Overall; will be dropped
            "lvl2" : "scenario",
            "lvl3" : "impact",
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
        # }}}

        ########################################################################
        # clean up financial_metrics  # {{{
        financial_metrics = financial_metrics[["ecm", "lvl2", "lvl3", "lvl4"]]
        financial_metrics = financial_metrics.rename(columns =
                {"lvl2" : "impact", "lvl3" : "year", "lvl4" : "value"})

        # set data types
        assert all(financial_metrics.value.apply(isfloat))
        financial_metrics.value = financial_metrics.value.apply(float)

        assert all(financial_metrics.year.str.contains("^\d{4}$"))
        financial_metrics.year = financial_metrics.year.apply(int)

        self.financial_metrics =\
                financial_metrics.sort_values(by = ["ecm", "impact", "year"])
        # }}}

    # }}}

    def by_category_vs_overall(self, tol = 1e-8): # {{{

        mas = self.mas_by_category\
                .groupby(["ecm", "scenario", "impact", "year"])\
                .agg({"value" : "sum"})\
                .reset_index()\
                .merge(self.mas_overall,
                        how = "outer",
                        on = ["ecm", "scenario", "impact", "year"],
                        suffixes = ("_aggregated", "_overall")
                        )
        mas["delta"] = mas.value_aggregated - mas.value_overall
        mas = mas[mas.delta > tol]

        osg = self.osg_by_category\
                .groupby(["impact", "year"])\
                .agg({"value" : "sum"})\
                .reset_index()\
                .merge(self.osg_overall,
                        how = "outer",
                        on = ["impact", "year"],
                        suffixes = ("_aggregated", "_overall")
                        )
        osg["delta"] = osg.value_aggregated - osg.value_overall
        osg = osg[osg.delta > tol]

        self.by_category_aggreation_vs_overall = {"Markets and Savings" : mas, "On-site Generation"  : osg}
    # }}}

    def aggregate_for_emf(self):                                         # {{{

        if self.emf_aggregation is None:

            maps = mapping_variables()

            df = self.mas_by_category\
                    .merge(maps.emf_base_string, how = "inner", on = "impact")
            df = df.merge(maps.building_class_construction,
                    how = "left",
                    left_on = "building_class",
                    right_on = "building_class0",
                    suffixes = ("_x", "")
                    )
            df = df.drop(columns = ["building_class0", "building_class_x"])

            # map fuel types
            df = df.merge(maps.fuel_types, how = "left", on = "fuel_type")
            not_mapped = set(df[((df.emf_fuel_type.isna()) & (df.fuel_type.notna()))]["fuel_type"])
            if len(not_mapped):
                msg = ", ".join(not_mapped)
                warnings.warn("Fuel types not mapped to EMF fuel types: " + msg)

            # map direct_indirect fuel
            df = df.merge(maps.direct_indirect_fuel, how = "left", on = "fuel_type")
            not_mapped = set(df[((df.direct_indirect_fuel.isna()) & (df.fuel_type.notna()))]["fuel_type"])
            if len(not_mapped):
                print(not_mapped)
                msg = ", ".join(not_mapped)
                warnings.warn("Fuel Types not mapped to direct/indirect: " + msg)

            # map end uses
            df = df.merge(maps.end_uses, how = "left", on = "end_use")
            not_mapped = set(df[df.emf_end_use.isna()]["end_use"])
            if len(not_mapped):
                msg = ", ".join(not_mapped)
                warnings.warn(f"Unmapped end uses: " + msg)

            # Convert MMBtu to Exajoules
            idx = df.impact.str.contains("MMBtu")
            df.loc[idx, "value"] *= 1.05505585262e-9
            df.impact = df.impact.str.replace("MMBtu", "EJ")

            # Aggregations
            # NOTE: units for the value column are unique between the
            # emf_base_strings. This is okay and accounted for since all
            # aggregations are done, in part, with a groupby emf_base_string.
            a0 = df\
                    .groupby(["region", "emf_base_string", "year"])\
                    .agg(value = ("value", "sum"))

            a1 = df\
                    .groupby(["region", "emf_base_string", "building_class", "year"])\
                    .agg(value = ("value", "sum"))

            a2 = df\
                    .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "year"])\
                    .agg(value = ("value", "sum"))

            a3_0 = df\
                    [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
                    .groupby(["region", "emf_base_string", "direct_indirect_fuel", "year"])\
                    .agg(value = ("value", "sum"))
            a3_1 = df\
                    [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
                    .groupby(["region", "emf_base_string", "building_class", "direct_indirect_fuel", "year"])\
                    .agg(value = ("value", "sum"))
            a3_2 = df\
                    [df.emf_base_string == "*Emissions|CO2|Energy|Demand|Buildings"]\
                    .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "direct_indirect_fuel", "year"])\
                    .agg(value = ("value", "sum"))

            a4_0 = df\
                    [df.emf_base_string == "*Final Energy|Buildings"]\
                    .groupby(["region", "emf_base_string", "emf_fuel_type", "year"])\
                    .agg(value = ("value", "sum"))
            a4_1 = df\
                    [df.emf_base_string == "*Final Energy|Buildings"]\
                    .groupby(["region", "emf_base_string", "building_class", "emf_fuel_type", "year"])\
                    .agg(value = ("value", "sum"))
            a4_2 = df\
                    [df.emf_base_string == "*Final Energy|Buildings"]\
                    .groupby(["region", "emf_base_string", "building_class", "emf_end_use", "emf_fuel_type", "year"])\
                    .agg(value = ("value", "sum"))

            # Aggregation clean up
            a0.reset_index(inplace = True)
            a1.reset_index(inplace = True)
            a2.reset_index(inplace = True)
            a3_0.reset_index(inplace = True)
            a3_1.reset_index(inplace = True)
            a3_2.reset_index(inplace = True)
            a4_0.reset_index(inplace = True)
            a4_1.reset_index(inplace = True)
            a4_2.reset_index(inplace = True)

            # build the full emf_string
            a0["emf_string"] = a0.region + a0.emf_base_string
            a1["emf_string"] = a0.region + a1.emf_base_string + "|" + a1.building_class
            a2["emf_string"] = a0.region + a2.emf_base_string + "|" + a2.building_class + "|" + a2.emf_end_use

            a3_0["emf_string"] = a3_0.region + a3_0.emf_base_string + "|" + a3_0.direct_indirect_fuel
            a3_1["emf_string"] = a3_1.region + a3_1.emf_base_string + "|" + a3_1.building_class + "|" + a3_1.direct_indirect_fuel
            a3_2["emf_string"] = a3_2.region + a3_2.emf_base_string + "|" + a3_2.building_class + "|" + a3_2.emf_end_use + "|" + a3_2.direct_indirect_fuel

            a4_0["emf_string"] = a4_0.region + a4_0.emf_base_string + "|" + a4_0.emf_fuel_type
            a4_1["emf_string"] = a4_1.region + a4_1.emf_base_string + "|" + a4_1.building_class + "|" + a4_1.emf_fuel_type
            a4_2["emf_string"] = a4_2.region + a4_2.emf_base_string + "|" + a4_2.building_class + "|" + a4_2.emf_end_use + "|" + a4_2.emf_fuel_type

            # build one data frame with all the aggregations
            a = pd.concat([
                a0[["emf_string", "year", "value"]],
                a1[["emf_string", "year", "value"]],
                a2[["emf_string", "year", "value"]],
                a3_0[["emf_string", "year", "value"]],
                a3_1[["emf_string", "year", "value"]],
                a3_2[["emf_string", "year", "value"]],
                a4_0[["emf_string", "year", "value"]],
                a4_1[["emf_string", "year", "value"]],
                a4_2[["emf_string", "year", "value"]]
                ])
            a.year = a.year.apply(str) # this is needed so the column names post pivot are strings
            a = a.pivot_table(index = ["emf_string"], columns = ["year"], values = ["value"])
            a.columns = a.columns.droplevel(0)
            a.reset_index(inplace = True)

            self.emf_aggregation = a
    # }}}

    def generate_plots(self, plot_dir): # {{{
        if not os.path.isdir(plot_dir):
            os.mkdir(plot_dir)

        shutil.copy("./templates/plots.html", plot_dir)

        # Financial Metrics # {{{
        if not os.path.isdir(os.path.join(plot_dir, "financial_metrics")):
            os.mkdir(os.path.join(plot_dir, "financial_metrics"))

        if not os.path.isdir(os.path.join(plot_dir, "financial_metrics", "each_ecm")):
            os.mkdir(os.path.join(plot_dir, "financial_metrics", "each_ecm"))

        # plot 1: aggregated for the year
        fig = px.line(
                data_frame = self.financial_metrics\
                        .groupby(["impact", "year"])\
                        .value\
                        .agg(["mean"])
                        .reset_index()
                , x = "year"
                , y = "mean"
                , title = "Mean Financial Metrics by Year"
                , facet_row = "impact")
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text = a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.write_html(os.path.join(plot_dir, "financial_metrics", "aggregated.html"))

        # plot 2: all ecms on one plot
        fig = px.line(
                data_frame = self.financial_metrics
                , x = "year"
                , y = "value"
                , color = "ecm"
                , facet_row = "impact")
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.write_html(os.path.join(plot_dir, "financial_metrics", "all_ecms.html"))

        # plot 3a, b, ... one file for each ecm
        for ecm in set(self.financial_metrics.ecm):
            fig = px.line(
                    data_frame = self.financial_metrics[self.financial_metrics.ecm == ecm]
                    , x = "year"
                    , y = "value"
                    , color = "ecm"
                    , facet_row = "impact")
            fig.update_yaxes(matches = None, exponentformat = "e")
            fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
            fig.write_html(os.path.join(plot_dir, "financial_metrics", "each_ecm", ecm + ".html"))

        with open(os.path.join(plot_dir, "financial_metrics", "each_ecm.js"), "w") as f:
            f.write('var all_fm_ecm_select_list = document.createElement("select");\n')
            f.write('var all_fm_ecms =' + "['--', '" + "', '".join(sorted(set(list(self.financial_metrics["ecm"])))) + "']\n")
            f.write('all_fm_ecm_select_list.setAttribute("id", "all_fm_ecm_select");\n')
            f.write('all_fm_ecm_select_list.setAttribute("onchange", "if (this.selectedIndex) get_fm_ecm();");\n')
            f.write('document.getElementById("all_fm_ecms_div").appendChild(all_fm_ecm_select_list);\n')
            f.write('for (var i = 0; i < all_fm_ecms.length; i++) {\n')
            f.write('\tvar option = document.createElement("option");\n')
            f.write('\toption.setAttribute("value", all_fm_ecms[i]);\n')
            f.write('\toption.text = all_fm_ecms[i];\n')
            f.write('\tall_fm_ecm_select_list.appendChild(option);\n')
            f.write('}\n\n')
            f.close()
        # }}}

        # Cost Effective Plots # {{{
        def unique_strings(l):
            list_set = set(l)
            ul = (list(list_set))
            return '; '.join(ul)

        # build one data set for plotting
        plot_data =\
                self.mas_by_category\
                .groupby(["scenario", "ecm", "impact", "year"])\
                .agg({
                    "value" : "sum",
                    "building_class" : unique_strings,
                    "region" : unique_strings,
                    "end_use" : unique_strings
                    })\
                .reset_index()\
                .pivot_table(
                        values = "value",
                        index = ["scenario", "ecm", "building_class", "end_use", "year"],
                        columns = ["impact"]
                )\
                .reset_index()\
                .merge(self.financial_metrics,
                        how = "left",
                        on = ["ecm", "year"]
                        )

        if not os.path.isdir(os.path.join(plot_dir, "cost_effectiveness")):
            os.mkdir(os.path.join(plot_dir, "cost_effectiveness"))

        for v in [{"carbon" : "Avoided CO\u2082 Emissions (MMTons)"},
                        {"cost"   : "Energy Cost Savings (USD)"},
                        {"energy" : "Energy Savings (MMBtu)"}]:
            n, voi = list(v.items())[0]
            if not os.path.isdir(os.path.join(plot_dir, "cost_effectiveness", n)):
                os.mkdir(os.path.join(plot_dir, "cost_effectiveness", n))

            for yr in set(plot_data.year):
                fig = px.scatter(
                        plot_data[(plot_data["year"] == yr)]
                        , x = voi
                        , y = "value"
                        , symbol = "building_class"
                        , color = "end_use"
                        , facet_col = "scenario"
                        , facet_row = "impact"
                        , title = "Calendar Year " + str(yr)
                        , hover_data = {
                            "ecm": True,
                            voi : True,
                            "value": True,
                            "end_use": True,
                            "building_class": True
                            }
                        )
                fig.update_yaxes(title_text = "", matches = None, exponentformat = "e")
                fig.update_xaxes(exponentformat = "e")
                fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
                fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))

                fig.write_html(os.path.join(plot_dir, "cost_effectiveness", n, str(yr) + ".html"))

        with open(os.path.join(plot_dir, "cost_effectiveness", "years.js"), "w") as f:
            for v in ["carbon", "cost", "energy"]:
                f.write('var ce_' + v + '_select_list = document.createElement("select");\n')
                f.write('var ce_' + v + '=' + "['--', '" + "', '".join(sorted(set(list(plot_data["year"].apply(str))))) + "']\n")
                f.write('ce_' + v + '_select_list.setAttribute("id", "ce_' + v + '_select");\n')
                f.write('ce_' + v + '_select_list.setAttribute("onchange", "if (this.selectedIndex) get_cost_effectiveness(\'' + v + '\');");\n')
                f.write('document.getElementById("ce_' + v + '_div").appendChild(ce_' + v + '_select_list);\n')
                f.write('for (var i = 0; i < ce_' + v + '.length; i++) {\n')
                f.write('\tvar option = document.createElement("option");\n')
                f.write('\toption.setAttribute("value", ce_' + v + '[i]);\n')
                f.write('\toption.text = ce_' + v + '[i];\n')
                f.write('\tce_' + v + '_select_list.appendChild(option);\n')
                f.write('}\n\n')
            f.close()

        # }}}

        # Total Savings Plots # {{{
        total_savings = self.mas_by_category\
                .groupby(["scenario", "impact", "year"])\
                .agg({"value" : "sum"})\
                .reset_index()
        total_savings2 = self.mas_by_category\
                .groupby(["scenario", "impact", "year"])\
                .agg({"value" : "sum"})\
                .groupby(level = ["scenario", "impact"])\
                .cumsum()\
                .reset_index()

        # Overall
        #fig = px.scatter(
        #        cms_by_region,
        #        x = "year",
        #        y = "value",
        #        color = "region",
        #        facet_col = "adoption_scenario")
        #fig.update_traces(mode = "lines+markers")
        #fig.update_yaxes(exponentformat = "e", title = VOI)
        #fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        #print("Writing " + plot_path + "by_region.html")
        #fig.write_html(plot_path + "by_region.html")




        if not os.path.isdir(os.path.join(plot_dir, "total_savings")):
            os.mkdir(os.path.join(plot_dir, "total_savings"))



        # }}}




        # Total CO2 Emissions # {{{
        # }}}



        # Total Cost # {{{
        # }}}



        # Total Energy # {{{
        # }}}

        return plot_data

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
        print("  * emf_aggregation:")
        print("      - returns DataFrames for EMF reporting")
        print("  * generate_plots(plot_dir):")
        print("      - create _a lot_ of graphics, all in plotly, and easily explored in via a local html page <plot_dir>/ecm_results.html")
    #}}}

#}}}



################################################################################
#                                 End of File                                  #
################################################################################

