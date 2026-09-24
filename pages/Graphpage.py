import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import pyperclip
import subprocess

dash.register_page(__name__, path="/Graphpage", name="Network Graph Visualizer")


layout = [
    html.Div([
        dbc.Modal(id='texModal',
                children = [
                    dbc.ModalHeader(dbc.ModalTitle("BibTex")),
                    dbc.ModalBody(children=html.Div(children=[html.P('test', id='texMessage', style={'textAlign': 'left', 'width': '100%'}),
                                                              dbc.Button('Copy', id='copy', n_clicks=0, style={'width': '25%'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column', 'justifyContent': 'center'})) # Dynamic error text goes here
                ],
                is_open=False, # Hidden initially
                centered=True,
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'}  # Centers it vertically on the screen!
            ),

        dbc.Modal(id='RefModal',
                children = [
                    dbc.ModalHeader(dbc.ModalTitle("References")),
                    dbc.ModalBody(children=html.Div(children=[dcc.Textarea('test', id='RefMessage', style={'textAlign': 'left', 'width': '100%', 'height':'50vh'}, readOnly=True)]) )# Dynamic error text goes here
                ],
                is_open=False, # Hidden initially
                centered=True,
                size="lg",
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'}  # Centers it vertically on the screen!
            ),

        html.Div(children=[
            dcc.Graph(id='Graph', style={'height': '85vh'}),
        ], style={'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '88vh'}),


        html.Div(children=[
            html.Div(children=[html.Label('Null', id='Title')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '15%'}),
            html.Div(children=[html.Label('Null', id='Authors')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '7%'}),
            html.Div(children=[html.Label('Null', id='Keywords')], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 10, 'flex': 1, 'border': '5px solid gray', 'height': '7%'}),
            html.Div(children=[html.Label('Null', id='Summary')], style={'textAlign': 'left', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'lineHeight': '1.2', 'padding': 10, 'flex': 1, 'border': '5px solid gray', 'height': '50%'}),
            html.Div(children=[dcc.Button('Full Paper', id='PDF-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '5%'}),
            html.Div(children=[dcc.Button('Bibtex', id='Bibtex-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '5%'}),
            html.Div(children=[dcc.Button('Reference List', id='Reference-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '5%'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'})
    ], style={'display': 'flex', 'flexDirection': 'row',})]


@callback(
    Output('Title', 'children'),
    Output('Authors', 'children'),
    Output('Keywords', 'children'),
    Output('Summary', 'children'),
    Output('Graph', 'figure'),
    Input('Graph', 'clickData'),
    State('Data', 'data'),
    State('fig', 'data')
)
def update_paper(clickData, data, fig):
    if clickData is not None:
        clickdata = clickData['points'][0]['customdata']
        clickid = clickdata
        index = -1
        for i in range(len(data['id'])):
            if data['id'][i] == clickid:
                index = i
        authors = AuthorFormat(data['Authors'][index])
        keywords = KeywordFormat(data['Keywords'][index])
        return data['Title'][index], authors, keywords, data['Summary'][index], fig

    return 'Null', 'Null', 'Null', 'Null', fig

@callback(
    Output('Title', 'style'),
    Input('Graph', 'clickData'),
    State('Data', 'data')
)
def update_Title_font_size(clickData, data):
    if clickData is not None:
        clickdata = clickData['points'][0]['customdata']
        clickid = clickdata
        index = -1
        for i in range(len(data['id'])):
            if data['id'][i] == clickid:
                index = i
        TitleLen = len(data['Title'][index])

        size = 15 * (TitleLen**(-0.08))-7
        height = 5 * (TitleLen**(-0.08))-2.5

        return {
            'fontSize': f'clamp(12px, {size}vh, 64px)',
            'lineHeight': f'{height}',
            'overflowWrap': 'break-word'  # Ensures long words split instead of clipping
        }
    return {'fontSize': 'clamp(12px, 4vh, 64px)', 'lineHeight': '1'}

@callback(
    Output('Authors', 'style'),
    Input('Graph', 'clickData'),
    State('Data', 'data')
)
def update_Authors_font_size(clickData, data):
    if clickData is not None:
        clickdata = clickData['points'][0]['customdata']
        clickid = clickdata
        index = -1
        for i in range(len(data['id'])):
            if data['id'][i] == clickid:
                index = i

        authors = AuthorFormat(data['Authors'][index])
        TitleLen = len(authors)

        size = 10 * (TitleLen**(-0.08))-5
        height = 1

        return {
            'fontSize': f'clamp(10px, {size}vh, 32px)',
            'lineHeight': f'{height}',
            'overflowWrap': 'break-word'  # Ensures long words split instead of clipping
        }
    return {'fontSize': 'clamp(10px, 2.4vh, 32px)', 'lineHeight': '0.8'}

@callback(
    Output('PDF-button', 'n_clicks'),
    Input('PDF-button', 'n_clicks'),
    State('Title', 'children'),
    State('Data', 'data')
)
def openPDF(clicks, Title, data):
    if clicks >= 1:
        clicks = 0
        for i in range(len(data['id'])):
            if data['Title'][i] == Title:
                link = data['Link'][i]
        subprocess.Popen(["xdg-open", link])


    return clicks

@callback(
    Output('Bibtex-button', 'n_clicks'),
    Output('texModal', 'is_open'),
    Output('texMessage', 'children'),
    Input('Bibtex-button', 'n_clicks'),
    State('Title', 'children'),
    State('Data', 'data')
)
def openTexModal(clicks, Title, data):
    if clicks >= 1:
        clicks = 0
        for i in range(len(data['id'])):
            if data['Title'][i] == Title:
                Tex = data['Bibtex'][i]
        return clicks, True, Tex

    return clicks, False, ''

@callback(
    Output('copy', 'n_clicks'),
    Input('copy', 'n_clicks'),
    State('Title', 'children'),
    State('Data', 'data')
)
def copyTex(clicks, Title, data):
    if clicks >= 1:
        clicks = 0
        for i in range(len(data['id'])):
            if data['Title'][i] == Title:
                Tex = data['Bibtex'][i]
        pyperclip.copy(Tex)
        return clicks

    return clicks

@callback(
    Output('Reference-button', 'n_clicks'),
    Output('RefModal', 'is_open'),
    Output('RefMessage', 'value'),
    Input('Reference-button', 'n_clicks'),
    State('Title', 'children'),
    State('Data', 'data')
)
def openRefModal(clicks, Title, data):
    if clicks >= 1:
        clicks = 0
        for i in range(len(data['id'])):
            if data['Title'][i] == Title:
                refstring = RefFormat(data['Refs'][i])
        return clicks, True, refstring

    return clicks, False, ''


def RefFormat(refs):
    refstring = ''

    for i in range(len(refs)):
        refstring += '[' + str(i+1) + '] '
        refstring += refs[i]
        refstring += '\n \n'

    return refstring

def AuthorFormat(Authors):
    AuthorString = ''
    if len(Authors) > 4:
        for i in range(3):
            AuthorString += Authors[i]
            AuthorString += ', '

        AuthorString += 'et al.'

    else:
        for i in range(len(Authors)):
            AuthorString += Authors[i]
            if i < len(Authors) - 2:
                AuthorString += ', '
            elif i < len(Authors) - 1:
                AuthorString += ' and '

    return AuthorString

def KeywordFormat(Keywords):
    keywordString = ''
    for keyword in Keywords:
        keywordString += keyword + ', '

    return keywordString[:-2]