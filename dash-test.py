#!/usr/bin/env python

import sys, getopt
import scout
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

def unique_strings(l):
    list_set = set(l)
    ul = (list(list_set))
    return '; '.join(ul)

################################################################################

################################################################################
# dash application

app = dash.Dash(external_stylesheets = [dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "26rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Scout ECM Results Graphics", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Financial Metrics", href="/fm", active="exact"),
                dbc.NavLink("Cost Effective Savings", href="/ces", active="exact"),
                dbc.NavLink("Total Savings", href="/savings", active="exact"),
                dbc.NavLink("(Un)Competed Totals", href="/cms_v_ums", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

def home(): #{{{
    return html.Div([
        html.P("This is the content of the home page!  A overview of what this application does goes here."),
        ])
# }}}

def fm(): 
    return html.Div([ # {{{
        html.H1("Financial Metrics"),
        html.Div([
            dcc.Dropdown(id = "fm_dropdown",
                options = [
                    {"label" : "Aggregated by Year", "value" : "agg_year"},
                    {"label" : "All ECMS", "value" : "all_ecms"},
                    {"label" : "Select an ECM:", "value" : "each_ecm"}
                    ],
                value = "agg_year",
                clearable = False
                )],
            style = {"width" : "25%", "display" : "inline-block"}
            ),
        html.Div([
            html.Label("ECM:"),
            dcc.Dropdown(id = "ecm_dropdown", options = ecms, value = ecms[0]["value"], clearable = False)], id = "ecm_dropdown_div", style = {"min-width" : "500px", "display" : "none"}),
        html.Div(id = "fm-output-container", style = {'width' : '90%', 'height': '900px'})
        ])
# }}}

def ces():
    return html.Div([ # {{{
        html.H1("Cost Effective Savings"),
        html.Div([
            html.Label("Impact:"),
            dcc.Dropdown(id = "ces_cce_dropdown",
                options = [
                    {"label" : "Avoided CO\u2082 Emissions (MMTons)", "value" : "carbon"},
                    {"label" : "Energy Cost Savings (USD)",           "value" : "cost"},
                    {"label" : "Energy Savings (MMBtu)",              "value" : "energy"}
                    ],
                value = "carbon",
                clearable = False
                )],
            style = {"width" : "25%", "display" : "inline-block"}
            ),
        html.Div([
            html.Label("Year:"),
            dcc.Dropdown(id = "year_dropdown", options = years, value = years[0], clearable = False)], id = "ecm_dropdown_div", style = {"min-width" : "500px", "display" : "inline-block"}),
        html.Div(id = "ces-output-container", style = {'width' : '90%', 'height': '900px'})
    ])
# }}}

def savings():
    return html.Div([  # {{{
        html.H1("Total Savings"),
        html.Div([
            html.Label("Impact:"),
            dcc.Dropdown(id = "savings_dropdown",
                options = [
                    {"label" : "Avoided CO\u2082 Emissions (MMTons)", "value" : "carbon"},
                    {"label" : "Energy Cost Savings (USD)",           "value" : "cost"},
                    {"label" : "Energy Savings (MMBtu)",              "value" : "energy"}
                    ],
                value = "carbon",
                clearable = False
                )],
            style = {"width" : "25%", "display" : "inline-block"}
            ),
        html.Div([
            html.Label("Aggregate by:"),
            dcc.Dropdown(id = "savings_by_dropdown",
            options = [
                {"label" : "Overall",           "value" : "overall"},
                {"label" : "By Region ",        "value" : "region"},
                {"label" : "By Building Class", "value" : "building_class"},
                {"label" : "By End Use",        "value" : "end_use"}
                ],
            value = "overall",
            clearable = False
            )],
            id = "savings_by_dropdown_div",
            style = {"min-width" : "400px", "display" : "inline-block"}
            ),
        html.Div([
            html.Label("Annual or Cumulative Totals?"),
            dcc.Dropdown(id = "savings_annual_cumulative_dropdown",
            options = [
                {"label" : "Annual Totals",           "value" : "annual"},
                {"label" : "Cumulative Totals",        "value" : "cumulative"}
                ],
            value = "annual",
            clearable = False
            )],
            id = "savings_annual_cumulative_dropdown_div",
            style = {"min-width" : "400px", "display" : "inline-block"}
            ),
        html.Div(id = "savings-output-container", style = {'width' : '90%', 'height': '900px'})
    ])
# }}}

def cms_v_ums():
    return html.Div([ # {{{
    html.H1("Competed vs. Uncompeted Totals"),
    html.Div([
        html.Label("By ECM or Adoption Scenario?:"),
        dcc.Dropdown(id = "cms_v_ums_dropdown",
            options = [
                {"label" : "ECM", "value" : "ecm"},
                {"label" : "Adoption Scenario", "value" : "scenario"},
                ],
            value = "ecm",
            clearable = False
            )],
        style = {"width" : "25%", "display" : "block"}
        ),
    html.Div([
        html.Label("Select an ECM to plot:"),
        dcc.Dropdown(id = "cms_v_ums_by_ecm_dropdown", options = ecms, value = ecms[0]["value"], clearable = False)], id = "cms_v_ums_ecm_dropdown_div", style = {"width" : "600px", "display" : "none"}),
    html.Div(id = "cms_v_ums-output-container", style = {'width' : '90%', 'height': '900px'})
])
# }}}

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home()
    elif pathname == "/fm":
        return fm()
    elif pathname == "/ces":
        return ces()
    elif pathname == "/savings":
        return savings()
    elif pathname == "/cms_v_ums":
        return cms_v_ums()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised."),
        ]
    )

###
### Financial Metrics # {{{
###

@app.callback(
        Output(component_id = 'ecm_dropdown_div', component_property = "style"),
        Input(component_id = 'fm_dropdown', component_property = 'value')
        )
def show_hide_ecm_dropdown(value):
    if value == "each_ecm":
        return {"display" : "block"}
    else:
        return {"display" : "none"}

@app.callback(
        Output('fm-output-container', 'children'),
        Input('fm_dropdown', 'value'),
        Input('ecm_dropdown', 'value')
        )
def update_fm_output(fm_dropdown_value, ecm_dropdown_value):
    if fm_dropdown_value == "agg_year":
        fig = px.line(
                data_frame = ecm_results.financial_metrics\
                        .groupby(["impact", "year"])\
                        .value\
                        .agg(["mean"])
                        .reset_index()
                , x = "year"
                , y = "mean"
                , title = "Mean Financial Metrics by Year"
                , facet_col = "impact"
                , facet_col_wrap = 2
                )
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text = a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.update_layout(autosize = False, width = 900, height = 900)
        return dcc.Graph(figure = fig)
    elif fm_dropdown_value == "all_ecms":
        fig = px.line(
                data_frame = ecm_results.financial_metrics
                , x = "year"
                , y = "value"
                , color = "ecm"
                , facet_col = "impact"
                , facet_col_wrap = 2
                )
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.update_layout(autosize = False, width = 900, height = 900)
        return dcc.Graph(figure = fig)
    elif fm_dropdown_value == "each_ecm":
        fig = px.line(
                data_frame = ecm_results.financial_metrics[ecm_results.financial_metrics.ecm == ecm_dropdown_value]
                , x = "year"
                , y = "value"
                #, color = "ecm"
                , facet_col = "impact"
                , facet_col_wrap = 2
                )
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.update_layout(autosize = False, width = 900, height = 900)
        fm_each_ecm = html.Div([
            dcc.Graph(figure = fig)
            ])
        return fm_each_ecm
    else:
        return "impressive, everything you did is wrong"

# }}}

###
### Cost Effective Savings # {{{
###

@app.callback(
        Output('ces-output-container', 'children'),
        Input('ces_cce_dropdown', 'value'),
        Input('year_dropdown', 'value')
        )
def update_ces_output(ces_dropdown_value, year_dropdown_value):
    if ces_dropdown_value == "carbon":
        m = "Avoided CO\u2082 Emissions (MMTons)"
    elif ces_dropdown_value == "cost":
        m = "Energy Cost Savings (USD)"
    elif ces_dropdown_value == "energy":
        m = "Energy Savings (MMBtu)"
    else: 
        m = None

    ces_plot_data =\
        ecm_results.mas_by_category\
                .groupby(["scenario", "ecm", "impact", "year"])\
                .agg({
                    "value" : "sum",
                    "building_class" : unique_strings,
                    "region" : unique_strings,
                    "end_use" : unique_strings
                    })\
                .reset_index()
    ces_plot_data = \
            pd.pivot_table(ces_plot_data,
                    values = "value",
                    index = ["scenario", "ecm", "building_class", "end_use", "year"],
                    columns = ["impact"]
                    )\
            .reset_index()\
            .merge(ecm_results.financial_metrics,
                    how = "left",
                    on = ["ecm", "year"])

    fig = px.scatter(
                ces_plot_data[(ces_plot_data.year == year_dropdown_value)]
            , x = m
            , y = "value"
            , symbol = "building_class"
            , color = "end_use"
            , facet_col = "scenario"
            , facet_row = "impact"
            , hover_data = {
                "ecm": True,
                m : True,
                "value": True,
                "end_use": True,
                "building_class": True
                }
            )
    fig.update_yaxes(title_text = "", matches = None, exponentformat = "e")
    fig.update_xaxes(exponentformat = "e")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
    fig.update_layout(autosize = False, width = 1200, height = 800)
    return dcc.Graph(figure = fig)

# }}}

###
### Savings # {{{
### 
@app.callback(
        Output("savings-output-container", 'children'),
        Input("savings_dropdown", "value"),
        Input("savings_by_dropdown", "value"),
        Input("savings_annual_cumulative_dropdown", "value")
        )
def update_savings_output(savings_dropdown_value, savings_by_dropdown_value, savings_annual_cumulative_dropdown):
    if savings_dropdown_value == "carbon":
        m = "Avoided CO\u2082 Emissions (MMTons)"
    elif savings_dropdown_value == "cost":
        m = "Energy Cost Savings (USD)"
    elif savings_dropdown_value == "energy":
        m = "Energy Savings (MMBtu)"
    else: 
        m = None

    if savings_by_dropdown_value == "overall":
        savings_by_dropdown_value = None

    a_data = ecm_results.mas_by_category\
        .sort_values(by = ["scenario", "impact", "year"])\
        .groupby([j for j in ["scenario", "impact", "year", savings_by_dropdown_value] if j is not None])\
        .agg({"value" : "sum"})\
        .reset_index()


    c_data = ecm_results.mas_by_category\
        .sort_values(by = ["scenario", "impact", "year"])\
        .groupby([j for j in ["scenario", "impact", "year", savings_by_dropdown_value] if j is not None])\
        .agg({"value" : "sum"})\
        .groupby(level = [j for j in ["scenario", "impact", savings_by_dropdown_value] if j is not None])\
        .cumsum()\
        .reset_index()

    a_data["total"] = "annual"
    c_data["total"] = "cumulative"
    plot_data = pd.concat([a_data, c_data])

    fig = px.line(
              plot_data[((plot_data.impact == m) & (plot_data.total == savings_annual_cumulative_dropdown))]
            , x = "year"
            , y = "value"
            , color = savings_by_dropdown_value
            , facet_col = "scenario"
            , markers = True
            )
    fig.update_traces(mode = "lines+markers")
    fig.update_yaxes(exponentformat = "e", title = m)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
    fig.update_layout(autosize = False, width = 1200, height = 800)

    return dcc.Graph(figure = fig)

# }}}

###
### competed vs uncompeted totals # {{{
###

@app.callback(
        Output('cms_v_ums-output-container', 'children'),
        Input('cms_v_ums_dropdown', 'value'),
        Input('cms_v_ums_by_ecm_dropdown', 'value')
        )
def update_cms_v_ums_output(cms_v_ums_dropdown_value, cms_v_ums_by_ecm_dropdown_value):
    if cms_v_ums_dropdown_value == "ecm":

        cms = ecm_results.mas_by_category[ecm_results.mas_by_category.ecm == cms_v_ums_by_ecm_dropdown_value]
        ums = ecm_prep.mseg_out_break[ecm_prep.mseg_out_break.ecm == cms_v_ums_by_ecm_dropdown_value]
        ums = ums[(ums.lvl3 == "baseline") | (ums.lvl3 == "efficient")]

        cms = cms.copy(deep = True)
        ums = ums.copy(deep = True)
        cms = cms.reset_index(drop = True)
        ums = ums.reset_index(drop = True)

        cms.loc[:, "competed"] = "Competed"
        cms.loc[:, "baseline_efficient"] = "efficient"
        cms.loc[cms.impact.str.startswith("Baseline"), "baseline_efficient"] = "baseline"
        cms = cms[["ecm", "scenario", "impact", "region", "building_class", "end_use", "fuel_type", "year", "value", "baseline_efficient", "competed"]]

        if (ums.shape[0] > 0):
            ums = ums.rename(columns = {"lvl3" : "baseline_efficient"})
            ums.loc[:, "competed"] = "Uncompeted"
            ums = cms[["ecm", "scenario", "impact", "region", "building_class", "end_use", "fuel_type", "year", "value", "baseline_efficient", "competed"]]
            ms = cms.append(ums, sort = True)
        else:
            ms = cms

        ms = ms.groupby(["scenario", "ecm", "competed", "baseline_efficient", "year"])\
                .agg({
                    "value": "sum",
                    "building_class" : unique_strings,
                    "region" : unique_strings,
                    "end_use" : unique_strings
                    })
        ms.reset_index(inplace = True)

        fig = px.scatter(
                ms,
                x = "year",
                y = "value",
                color = "baseline_efficient",
                symbol = "competed",
                facet_col = "scenario",
                labels = {
                    "year": "Year",
                    #"value": VOI,
                    "baseline_efficient": "baseline_efficient",
                    "competed": "Competed"
                    }
                #,
                #title = ecm + "<br><sup>Building Class: " +\
                #        unique_strings(ms.loc[ms["ecm"] == ecm, "building_class"]) +\
                #        " | Region: " +\
                #        unique_strings(ms.loc[ms["ecm"] == ecm, "region"]) +\
                #        " | End Use: " +\
                #        unique_strings(ms.loc[ms["ecm"] == ecm, "end_use"]) +\
                #        "</sup>"
                )
        fig.update_yaxes(exponentformat = "e")
        fig.update_traces(mode = "lines+markers")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

        
        return dcc.Graph(figure = fig)
    else:
        return cms_v_ums_dropdown_value


@app.callback(
        Output(component_id = 'cms_v_ums_ecm_dropdown_div', component_property = "style"),
        Input(component_id = 'cms_v_ums_dropdown', component_property = 'value')
        )
def show_hide_cms_v_ums_ecm_dropdown(value):
    if value == "ecm":
        return {"display" : "block"}
    else:
        return {"display" : "none"}
# }}}











if __name__ == "__main__":

    ecm_results = ''
    ecm_prep    = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr:p:", ["help", "ecm_results=", "ecm_prep="])
    except getopt.GetoptError:
        print("dash-test -r <ecm_results file> -p <ecm_prep file>")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("dash-test -r <ecm_results file> -p <ecm_prep file>")
            print("Options:")
            print("  -h --help         Print this help and exit")
            print("  -r --ecm_results  Path to a ecm_results file, the results of run.py")
            print("  -p --ecm_prep     Path to a ecm_prep file, the results of ecm_prep.py")
            sys.exit()
        elif opt in ("-r", "--ecm_results"):
            ecm_results = arg
        elif opt in ("-p", "--ecm_prep"):
            ecm_prep = arg


    if (ecm_results == ''):
        print("path to ecm_results must be provided")
        sys.exit(1)

    if (ecm_prep == ''):
        print("path to ecm_prep must be provided")
        sys.exit(1)

    ################################################################################
    # Data Import
    print("Importing Results file" + ecm_results) 
    ecm_results = scout.ecm_results(path = ecm_results)

    print("Importing ECM prep file" + ecm_prep) 
    ecm_prep = scout.ecm_prep(path = ecm_prep)

    ################################################################################
    # build useful things for ui
    ecms = [{"label" : l, "value" : l} for l in set(ecm_results.financial_metrics.ecm)]
    years = [y for y in set(ecm_results.mas_by_category.year)]
    years.sort()

    print("Launching dash app")
    app.run_server(port=8050, debug = True)


################################################################################
#                                 end of file                                  #
################################################################################

