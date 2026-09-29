import dash
from dash import html, dcc, callback, Output
import dash_bootstrap_components as dbc
from typing import cast

import dash_mantine_components as dmc

from Database import readDatabase
from Network_calculator import makeGraph

app = dash.Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP, dbc.themes.BOOTSTRAP], use_pages=True)

my_custom_theme = {
    "colors": {
        "deepBlue": ["#E9EDFC", "#C1CCF6", "#99ABF0"]
    },
    "shadows": {
        "md": "1px 1px 3px rgba(0,0,0,.25)",
        "xl": "5px 5px 3px rgba(0,0,0,.25)"
    },
    "headings": {
        "fontFamily": "Roboto, sans-serif",
        "sizes": {
            "h1": {"fontSize": "30px"}
        }
    }
}

app.layout = dmc.MantineProvider(
    theme = cast(any, my_custom_theme),
    children = [
    dcc.Store(id='Data', storage_type='session'),
    dcc.Store(id='Edges', storage_type='session'),
    dcc.Store(id='fig', storage_type='session'),
    dmc.Group(children=[
        dmc.SimpleGrid([
            dcc.Link(dmc.Button("Add", fullWidth=True), href='NewPaper'),
            dcc.Link(dmc.Button("Edit", fullWidth=True), href='EditPaper'),
            dcc.Link(dmc.Button("Graph", fullWidth=True), href='Graphpage'),
        ],
        cols=2,
        spacing="xs",
        verticalSpacing="xs"),
        dmc.Box("Constellation Filing System", style={'fontSize': 40, 'lineHeight': 1}),
        html.Img(src='assets/logo.png', style={'height': '7.5vh'}),
    ],
    justify="space-between",
	gap="md",
    mx="xs"),
    dash.page_container
])

@callback(
    Output('Data', 'data'),
    Output('Edges', 'data'),
    Output('fig', 'data'),
)
def StartCallback():
    data, edges = readDatabase()
    fig = makeGraph(data, edges)

    return data, edges, fig

if __name__ == "__main__":
    app.run(port=11100)