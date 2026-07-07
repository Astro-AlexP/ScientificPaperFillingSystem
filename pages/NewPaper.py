import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from Paper_Info import fetchOpenalexDataDOI, fetchOpenalexDataTitle, getCredentials

dash.register_page(__name__, path="/NewPaper", name="Add New Paper")


layout = [
    html.Div([
        html.Div(children=[
            html.Div(children=[
                html.Label('Title:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Textarea(id='TitleInput', style={'width': '75%', 'height': '150%', 'resize': 'none'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '4vh'}),
            html.Div(children=[
                html.Label('Authors:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='AuthorsInput', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('DOI:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='DOIInput', type='text', style={'width': '75%'}),
                html.Div(style={'width': '3%'}),
                dcc.Button('Search', id='Search', n_clicks=0, style={'width': '7%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '3vh'}),
            html.Div(children=[
                html.Label('Keywords:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='KeywordsInput', type='text', style={'width': '75%'})],
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
                dcc.Textarea(id='SummaryInput', style={'width': '95%', 'height':'100%', 'resize': 'none'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '45vh'}),
            html.Div(children=[
                html.Div(style={'width': '2.5%'}),
                dcc.Button('Clear', id='Clear', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '5%'}),
                dcc.Button('Save', id='Save', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '2.5%'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'height': '7.5%'} )
        ], style={'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '85vh'}),

        html.Div(children=[
            html.Div(children=[
                html.Label('References')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '10vh', 'fontSize': '4vh'}),
            html.Div(children=[
                dcc.Textarea(id='ref1', style={'width': '45%', 'height': '150%', 'resize': 'none'}), dcc.Textarea(id='ref2', style={'width': '45%', 'height': '150%', 'resize': 'none'})],
            style={'textAlign': 'center', 'padding': 10, 'flex': 9, 'height': '45vh'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'})
    ], style={'display': 'flex', 'flexDirection': 'row', })]

@callback(
    Output('TitleInput', 'value'),
    Output('AuthorsInput', 'value'),
    Output('DOIInput', 'value'),
    Output('ref1', 'value'),
    Output('ref2', 'value'),
    Output('Search', 'n_clicks'),
    Input('Search', 'n_clicks'),
    State('TitleInput', 'value'),
    State('DOIInput', 'value'),
    prevent_initial_call=True
)
def searchForPaper(n_clicks, Title, DOI):
    if n_clicks > 0:
        n_clicks = 0
        creds = getCredentials()
        if DOI is not None:
            info = fetchOpenalexDataDOI(DOI, creds)

        elif Title is not None:
            info = fetchOpenalexDataTitle(Title, creds)

        if info is not None:
            refs = formatRefs(info['formatedRef'])
            return info['Title'], info['Authors'], info['DOI'], refs[0], refs[1], n_clicks

        else:
            error_message = 'Error: Paper not found'
            return error_message, None, None, None, n_clicks
    else:
        return Title, DOI, None, None, n_clicks


def formatRefs(references):
    ref1 = ''
    ref2 = ''

    for i in range(len(references)):
        if i % 2 == 0:
            ref1 += '[' + str(i+1) + '] '
            ref1 += references[i]
            ref1 += '\n'
            ref1 += '\n'

        if i % 2 == 1:
            ref2 += '[' + str(i+1) + '] '
            ref2 += references[i]
            ref2 += '\n'
            ref2 += '\n'

    return [ref1, ref2]