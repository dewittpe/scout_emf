import scout
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

def unique_strings(l):
    list_set = set(l)
    ul = (list(list_set))
    return '; '.join(ul)


# import data
results_1 = scout.ecm_results(path = "./Results_Files_3/ecm_results_1-1.json.gz")

# build useful things for ui
ecms = [{"label" : l, "value" : l} for l in set(results_1.financial_metrics.ecm)]
years = [y for y in set(results_1.mas_by_category.year)]
years.sort()

# plotting data sets
ces_plot_data =\
    results_1.mas_by_category\
            .groupby(["scenario", "ecm", "metric", "year"])\
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
                columns = ["metric"]
                )\
        .reset_index()\
        .merge(results_1.financial_metrics,
                how = "left",
                on = ["ecm", "year"])

ces_plot_data

        

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
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

fm = html.Div([
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
    html.Div([dcc.Dropdown(id = "ecm_dropdown", options = ecms, value = ecms[0]["value"], clearable = False)], id = "ecm_dropdown_div", style = {"min-width" : "500px", "display" : "none"}),
    html.Div(id = "fm-output-container", style = {'width' : '90%', 'height': '900px'})
])

ces = html.Div([
    html.H1("Cost Effective Savings"),
    html.Div([
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
    html.Div([dcc.Dropdown(id = "year_dropdown", options = years, value = years[0], clearable = False)], id = "ecm_dropdown_div", style = {"min-width" : "500px", "display" : "inline-block"}),
    html.Div(id = "ces-output-container", style = {'width' : '90%', 'height': '900px'})
])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!  A overview of what this application does goes here.")
    elif pathname == "/fm":
        return fm
    elif pathname == "/ces":
        return ces
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

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
                data_frame = results_1.financial_metrics\
                        .groupby(["metric", "year"])\
                        .value\
                        .agg(["mean"])
                        .reset_index()
                , x = "year"
                , y = "mean"
                , title = "Mean Financial Metrics by Year"
                , facet_col = "metric"
                , facet_col_wrap = 2
                )
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text = a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.update_layout(autosize = False, width = 900, height = 900)
        return dcc.Graph(figure = fig)
    elif fm_dropdown_value == "all_ecms":
        fig = px.line(
                data_frame = results_1.financial_metrics
                , x = "year"
                , y = "value"
                , color = "ecm"
                , facet_col = "metric"
                , facet_col_wrap = 2
                )
        fig.update_yaxes(matches = None, exponentformat = "e")
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.for_each_annotation(lambda a: a.update(text = a.text.replace(" (", "<br>(")))
        fig.update_layout(autosize = False, width = 900, height = 900)
        return dcc.Graph(figure = fig)
    elif fm_dropdown_value == "each_ecm":
        fig = px.line(
                data_frame = results_1.financial_metrics[results_1.financial_metrics.ecm == ecm_dropdown_value]
                , x = "year"
                , y = "value"
                #, color = "ecm"
                , facet_col = "metric"
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

    fig = px.scatter(
                ces_plot_data[(ces_plot_data.year == year_dropdown_value)]
            , x = m
            , y = "value"
            , symbol = "building_class"
            , color = "end_use"
            , facet_col = "scenario"
            , facet_row = "metric"
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



if __name__ == "__main__":
    app.run_server(port=8050)




