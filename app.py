import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# 1. Initialize the app with pages enabled
app = dash.Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP], use_pages=True)

# 2. Design the master framework layout
app.layout = html.Div([
    # Global Header (Visible on all pages)
    html.Div([
        html.Div("Arachni Filling System", style={'fontSize': 40, 'lineHeight': 1}),
        #html.Hr(),
        # Navigation Links: dash.page_registry maps out your folder files automatically
        html.Div([
            dcc.Link(f"{page['name']}", href=page["relative_path"], style={'marginRight': '15px'})
            for page in dash.page_registry.values()
        ]),
    ], style={'display': 'flex', 'flexDirection': 'column', 'justifyContent': 'space-between', 'backgroundColor': '#f8f9fa', 'margin': '0', 'textAlign': 'center', 'fontSize': 20, 'height': '10vh'}),

    # The Dynamic Content Area (Where pages display)
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)