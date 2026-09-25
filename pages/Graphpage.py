import dash
from dash import html, dcc, callback, Output, Input, State, Patch
import dash_bootstrap_components as dbc
from Network_calculator import makeGraph
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

        dbc.Modal(id='HelpModal',
                children = [
                    dbc.ModalHeader(dbc.ModalTitle("Key")),
                    dbc.ModalBody(children=html.Div(
                        children=[html.Div(children = [
                            html.Div(children=[
                                html.Label('Shape', style={"fontSize": "30px"}),
                                html.Div(children=[
                                    html.Div(children=[
                                        html.Div(children=[html.Label('●', style={"fontSize": "50px"}), html.Label('Paper', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                        html.Div(children=[html.Label('⬟', style={"fontSize": "50px"}), html.Label('Preprint', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                    ], style={'height': '100%', 'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                    html.Div(children=[
                                        html.Div(children=[html.Label('⯃', style={"fontSize": "50px"}), html.Label('Review', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                        html.Div(children=[html.Label('⬢', style={"fontSize": "50px"}), html.Label('Thesis', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                    ], style={'height': '100%', 'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                    html.Div(children=[
                                        html.Div(children=[html.Label('◆', style={"fontSize": "50px"}), html.Label('Textbook', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                        html.Div(children=[html.Label('■', style={"fontSize": "50px"}), html.Label('Other', style={"fontSize": "20px"})], style={'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                    ], style={'height': '100%', 'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                                ], style={'width': '100%', 'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'}),
                                html.Div(style={'height': '5%'}),
                                html.Label('Size', style={"fontSize": "30px"}),
                                html.Div(children=[
                                    html.Label('Least Refs', style={"fontSize": "20px", 'padding': 20}),
                                    html.Label('●', style={"fontSize": "30px"}),
                                    html.Label('●', style={"fontSize": "40px"}),
                                    html.Label('●', style={"fontSize": "50px"}),
                                    html.Label('●', style={"fontSize": "60px"}),
                                    html.Label('●', style={"fontSize": "70px"}),
                                    html.Label('Most Refs', style={"fontSize": "20px", 'padding': 20}),
                                ], style={'display': 'flex', 'flex': '2', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'}),
                            ],style={'height': '100%', 'display': 'flex', 'flex': '3', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}),
                            html.Div(children=[
                                html.Label('Colour', style={"fontSize": "30px"}),
                                html.Div([], style={'height': '5%'}),
                                html.Label('Oldest'),
                                html.Div(children=[], style={'background': 'linear-gradient(0deg,rgba(0, 153, 255, 1) 0%, rgba(255, 0, 47, 1) 100%)', 'height': '92%', 'minWidth': '10vh', 'display': 'flex', 'alignItems': 'center'}),
                                html.Label('Newest')
                            ], style={'height': '100%', 'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 20, 'justifyContent': 'center'})],
                            style={'height': '40vh', 'width': '100%', 'display': 'flex', 'flex': '2', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'})]) ),
                ],
                is_open=False,
                centered=True,
                size="lg",
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'column', 'padding': 10, 'justifyContent': 'center'}  # Centers it vertically on the screen!
            ),

        html.Div(children=[
            html.Div(children=[
                dcc.Dropdown(id='FilterChoice', placeholder='Categories', style={'width': '45%', 'height': '75%', 'resize': 'none', 'display': 'flex'}),
                html.Div(style={'width': '2%', 'height': '75%', 'resize': 'none', 'display': 'flex'}),
                dcc.Dropdown(id='Filter', placeholder='Filters', multi=True, style={'width': '45%', 'height': '75%', 'resize': 'none', 'display': 'flex'}),
                html.Div(style={'width': '2%', 'height': '75%', 'resize': 'none', 'display': 'flex'}),
                dcc.Button('help', id='help', style={'width': '5%', 'height': '75%', 'resize': 'none', 'display': 'flex'})
            ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'justifyContent': 'center'}),
            dcc.Graph(id='Graph', style={'height': '80vh'}),
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
    Output('HelpModal', 'is_open'),
    Output('help', 'n_clicks'),
    Input('help', 'n_clicks'),
    prevent_initial_call=True
)
def openHelp(nclick):
    if nclick > 0:
        nclick = 0
        return True, nclick

    return False, nclick

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

@callback(
    Output('FilterChoice', 'options'),
    Output('Filter', 'options'),
    Output('Graph', 'figure', allow_duplicate=True),
    Output('Data', 'data', allow_duplicate=True),
    Output('Edges', 'data', allow_duplicate=True),
    Output('fig', 'data', allow_duplicate=True),
    Input('FilterChoice', 'options'),
    Input('FilterChoice', 'value'),
    Input('Filter', 'options'),
    Input('Filter', 'value'),
    State('Data', 'data'),
    State('Edges', 'data'),
    State('fig', 'data'),
    prevent_initial_call=True
)
def filterControl(choiceOptions, choice, filterOptions, filter, data, edges, fig):
    if choiceOptions is None:
        choiceOptions = ['Year', 'Authors', 'Keywords', 'Title', 'References']
    if filterOptions is None:
        filterOptions = []
    if filter is None:
        filter = []

    if choice is not None:
        if choice == 'Year' or choice == 'Title':
            filterOptions = data[choice]

        elif choice == 'Authors' or choice == 'Keywords':
            fullList = []
            for i in range(len(data[choice])):
                fullList += data[choice][i]

            filterOptions = list(set(fullList))

        elif choice == 'References':
            filterOptions = data['PaperImpact']

    if len(filter) > 0:
        ids = findIndex(choice, filter, data)

        opacity = []
        for id in data['id']:
            if id in ids:
                opacity.append(1)
            else:
                opacity.append(0.2)

    else:
        opacity = []
        for id in data['id']:
            opacity.append(1)

    fig = makeGraph(data, edges, opacity)

    return choiceOptions, filterOptions, fig, data, edges, fig


def findIndex(choice, filter, data):
    ids = []
    if choice == 'Year' or choice == 'Title':
        for i in range(len(data[choice])):
            if data[choice][i] in filter:
                ids.append(data['id'][i])

    elif choice == 'Authors' or choice == 'Keywords':
        for i in range(len(data[choice])):
            found = False
            for j in range(len(data[choice][i])):
                if data[choice][i][j] in filter:
                    found = True
        if found:
            ids.append(data['id'][i])

    elif choice == 'References':
        for i in range(len(data['PaperImpact'])):
            if data['PaperImpact'][i] in filter:
                ids.append(data['id'][i])

    return ids

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