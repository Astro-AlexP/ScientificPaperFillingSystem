import subprocess

import dash
import pyperclip
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from assets import Modals

from Network_calculator import makeGraph

dash.register_page(__name__, path="/Graphpage", name="Network Graph Visualizer")

layout = [
    html.Div([
        Modals.texModal,

        Modals.refModal,

        Modals.keyModal,

        dmc.Grid(
            columns=10,
            children = [
                dmc.GridCol([
                    dmc.Paper([
                        dmc.Stack([
                            dmc.Grid(
                                columns = 20,
                                children = [
                                    dmc.GridCol(dcc.Dropdown(id='FilterChoice', placeholder='Categories'), span=9),
                                    dmc.GridCol(dcc.Dropdown(id='Filter', placeholder='Filters', multi=True), span=9),
                                    dmc.GridCol(dmc.Button('help', id='help'), span=2),
                                ],
                                align='stretch',
                                justify="space-between",
                            ),
                            dcc.Graph(id='Graph', style={'height': '95%'}),
                        ],
                        align='stretch',
                        style={'height': '87vh'}
                        )
                    ],
                    radius="md",
                    p="sm",
                    shadow="lg",
                    withBorder=True,
                    )
                ],
                span=6),
                dmc.GridCol([
                    dmc.Paper([
                        dmc.Stack([
                            html.Div(children=[html.Label('Null', id='Title')], style={'textAlign': 'center', 'padding': 10, 'height': '15%'}),
                            html.Div(children=[html.Label('Null', id='Authors')], style={'textAlign': 'center', 'padding': 10, 'height': '7%'}),
                            html.Div(children=[html.Label('Null', id='Keywords')], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 8, 'border': '1px solid gray', 'height': '7%'}),
                            html.Div(children=[dcc.Textarea('Null', id='Summary', readOnly=False, style={'width': '100%', 'height': '100%', 'border': 'none', 'outline': 'none', 'resize': 'none'})],
                                     style={'textAlign': 'left', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'lineHeight': '1.2', 'padding': 8,'border': '1px solid gray', 'height': '58%'}),
                            html.Div(children=[dmc.Button('Full Paper', id='PDF-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'height': '3%'}),
                            html.Div(children=[dmc.Button('Bibtex', id='Bibtex-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'height': '3%'}),
                            html.Div(children=[dmc.Button('Reference List', id='Reference-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'height': '3%'})
                        ],
                        justify="flex-start",
                        style={'height': '87vh'}
                        )
                    ],
                        radius="md",
                        p="sm",
                        shadow="lg",
                        withBorder=True,
                    )
                ],
                span=4),
            ],
            align='stretch',
            justify="center",
        )

    ], style={'margin': 10})]

@callback(
    Output('Title', 'children'),
    Output('Authors', 'children'),
    Output('Keywords', 'children'),
    Output('Summary', 'value'),
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
    Output('helpModal', 'opened'),
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

        size = 15 * (TitleLen ** (-0.08)) - 7
        height = 5 * (TitleLen ** (-0.08)) - 2.5

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

        size = 10 * (TitleLen ** (-0.08)) - 5
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
    Output('texModal', 'opened'),
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
    Output('refModal', 'opened'),
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
        refstring += '[' + str(i + 1) + '] '
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
