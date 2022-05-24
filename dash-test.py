import scout
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

results_1 = scout.ecm_results(path = "./Results_Files_3/ecm_results_1-1.json.gz")






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
    html.H2("Controls"),
    dcc.Dropdown(id = "dropdown01",
        options = [
            {"label" : "Aggregated by Year", "value" : "agg_year"},
            {"label" : "All ECMS", "value" : "all_ecms"},
            {"label" : "Select an ECM", "value" : "each_ecms"}],
        value = "Aggregated by Year"),
    html.Div(id = "fm-output-container", 
        style = {'width' : '50%', 'height': '900px'})
])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!  A overview of what this application does goes here.")
    elif pathname == "/fm":
        return fm#html.P("Financial Metrics")
    elif pathname == "/ces":
        return html.P("Cost Effective Savings")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
        Output('fm-output-container', 'children'),
        Input('dropdown01', 'value')
        )

def update_output(value):
    if value == "agg_year":
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
    elif value == "all_ecms":
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
    else:
        return f"you selected {value}"




if __name__ == "__main__":
    app.run_server(port=8050)




