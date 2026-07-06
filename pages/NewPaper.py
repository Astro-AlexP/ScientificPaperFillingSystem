import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/NewPaper", name="Add New Paper")


layout = [
    html.Div([
        html.Div(children=[
            html.Div(children=[
                html.Label('Title:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Textarea(id='Title', style={'width': '75%', 'height': '150%', 'resize': 'none'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '4vh'}),
            html.Div(children=[
                html.Label('Authors:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='Authors', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('DOI:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='DOI', type='text', style={'width': '75%'}),
                html.Div(style={'width': '3%'}),
                dcc.Button('Search', id='Search', n_clicks=0, style={'width': '7%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('Keywords:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='Keywords', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('File:', style={'fontSize': '2.5vh', 'width': '12%'}),
                html.Div(dcc.Upload(id='upload-data',children=html.Div([
                    html.I(className="bi bi-cloud-arrow-up")],
                    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'alignItems': 'center', 'width': '100%', 'height': '100%'})),
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'width': '2%', 'boxSizing': 'border-box', 'justifyContent': 'center', 'height': '35px', 'border': '1px solid #888888', 'borderRadius': '5px', 'cursor': 'pointer'}),
                dcc.Input(type='text', style={'width': '73%', 'height': '35px'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('Summary:', style={'fontSize': '2.5vh', 'width': '12%'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                dcc.Textarea(id='Summary', style={'width': '95%', 'height':'100%', 'resize': 'none'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '45vh'}),
            html.Div(children=[
                html.Div(style={'width': '2.5%'}),
                dcc.Button('Clear', id='Clear', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '5%'}),
                dcc.Button('Save', id='Save', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '2.5%'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'height': '10%'} )
        ], style={'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '85vh'}),

        html.Div(children=[
            html.Div(children=[
                html.Label('References')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '10vh', 'fontSize': '4vh'}),
            html.Div(children=[
                dcc.Textarea(id='ref1', style={'width': '45%', 'height': '150%', 'resize': 'none'}), dcc.Textarea(id='ref2', style={'width': '45%', 'height': '150%', 'resize': 'none'})],
            style={'textAlign': 'center', 'padding': 10, 'flex': 9, 'height': '45vh'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'})
    ], style={'display': 'flex', 'flexDirection': 'row', })]