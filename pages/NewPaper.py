import dash
from dash import html, dcc, callback, Output, Input, State, ctx
import dash_mantine_components as dmc
from Paper_Info import fetchOpenalexDataDOI, fetchOpenalexDataTitle, getCredentials
from Database import savePaper, readDatabase
from Network_calculator import makeGraph
from assets import Modals

dash.register_page(__name__, path="/NewPaper", name="Add New Paper")


layout = [
    html.Div([
        Modals.errorModal,

        dcc.Store(id='paperData', storage_type='session'),

        dcc.Store(id='fileData', storage_type='session'),

        dmc.Grid(
            columns=10,
            children=[
                dmc.GridCol([
                    dmc.Paper([
                        dmc.Stack([
                            dmc.Group([
                                dmc.Text('Title:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='TitleInput', style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Authors:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='AuthorsInput',
                                             style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('DOI:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='DOIInput', style={'width': '75%', 'height': '30px', 'resize': 'none'}),
                                dmc.Button('Search', id='Search', n_clicks=0)
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Keywords:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='KeywordsInput',
                                             style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('File:', style={'fontSize': 30, 'width':'140px'}),
                                html.Div([html.Div([dcc.Upload(id='upload', accept="application/pdf", children=html.Div([html.I(className="bi bi-cloud-arrow-up")],)),
                                          ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'width': '3%', 'boxSizing': 'border-box', 'justifyContent': 'center', 'height': '35px', 'border': '1px solid #888888', 'borderRadius': '5px', 'cursor': 'pointer'}),
                                    dcc.Input(id='filePath', type='text', style={'width': '97%', 'height': '35px'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row','width': '75%'}),

                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Summary:', style={'fontSize': 30, 'width':'140px'}),
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dcc.Textarea(id='SummaryInput', style={'width': '95%', 'height':'100%', 'resize': 'none'}),
                            ],
                                align='center',
                                justify='center',
                                gap="md",
                                style={'height': '60%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Button('Clear', id='Clear', n_clicks=0, style={'width': '30%', 'height': '100%'}),
                                dmc.Button('Save', id='Save', n_clicks=0, style={'width': '30%', 'height': '100%'}),
                            ],
                                align='center',
                                justify='space-around',
                                gap="lg",
                                style={'height': '6%', 'width': '100%'}),
                        ],
                            align='flex-start',
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
                            dmc.Text('References', ta="center", style={"fontSize": 40}),
                            dmc.Group([
                                dcc.Textarea(id='ref1', readOnly=True, style={'height': '100%', 'resize': 'none'}),
                                dcc.Textarea(id='ref2', readOnly=True, style={'height': '100%', 'resize': 'none'})
                            ],
                                justify="center",
                                gap="sm",
                                grow=True,
                                style={'height': '90%'}
                            )
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
    Output('TitleInput', 'value'),
    Output('AuthorsInput', 'value'),
    Output('DOIInput', 'value'),
    Output('KeywordsInput', 'value'),
    Output('SummaryInput', 'value'),
    Output('ref1', 'value'),
    Output('ref2', 'value'),
    Output('Search', 'n_clicks'),
    Output('Clear', 'n_clicks'),
    Output('Save', 'n_clicks'),
    Output('paperData', 'data'),
    Output('fileData', 'data'),
    Output('filePath', 'value'),
    Output('errorModal', 'is_open'),
    Output('errMessage', 'children'),
    Output('Data', 'data', allow_duplicate=True),
    Output('Edges', 'data', allow_duplicate=True),
    Output('fig', 'data', allow_duplicate=True),
    Input('Search', 'n_clicks'),
    Input('Clear', 'n_clicks'),
    Input('Save', 'n_clicks'),
    Input('upload', 'filename'),
    Input('upload', 'contents'),
    State('TitleInput', 'value'),
    State('AuthorsInput', 'value'),
    State('DOIInput', 'value'),
    State('filePath', 'value'),
    State('KeywordsInput', 'value'),
    State('SummaryInput', 'value'),
    State('paperData', 'data'),
    State('fileData', 'data'),
    State('Data', 'data'),
    State('Edges', 'data'),
    State('fig', 'data'),
    prevent_initial_call=True
)
def formControls(Search, ClearB, Save, UploadName, UploadContent, Title, Authors, DOI, filePath, Keywords, Summary, paperData, fileData, data, Edges, fig):
    if paperData is None:
        paperData = {'formatedRef': []}
        paperData['formatedRef'] = ['', '']
    if Search > 0:
        Search = 0
        creds = getCredentials()
        info, refs = paperSearch(Title, DOI, creds)
        if info is not None and refs is not None:
            refs = formatRefs(info['formatedRef'])
            return info['Title'], info['Authors'], info['DOI'], Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, info, fileData, filePath, False, None, data, Edges, fig

        else:
            refs = formatRefs(paperData['formatedRef'])
            return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, None, None, filePath, True, 'No paper found', data, Edges, fig

    if ClearB > 0:
        ClearB = 0
        return '', '', '', '', '', '', '', Search, ClearB, Save, None, None, None, False, None, data, Edges, fig

    if Save > 0:
        Save = 0
        if Title is not None and Authors is not None and DOI is not None and filePath is not None and Keywords is not None and Summary is not None and paperData is not None:
            savePaper(Title, Authors, DOI, Keywords, Summary, filePath, paperData, fileData)
            data, edges = readDatabase()
            try:
                fig = makeGraph(data, edges)

            except:
                pass
            return '', '', '', '', '', '', '', Search, ClearB, Save, None, None, None, False, None, data, Edges, fig
        else:
            refs = formatRefs(paperData['formatedRef'])
            return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, fileData, filePath, True, 'Data not entries not complete', data, Edges, fig

    if UploadName is not None:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, UploadContent, UploadName, False, None, data, Edges, fig

    else:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, fileData, filePath, False, None, data, Edges, fig



def paperSearch(Title, DOI, creds):
    try:
        if DOI is not None and DOI != '':
            info = fetchOpenalexDataDOI(DOI, creds)

        elif Title is not None:
            info = fetchOpenalexDataTitle(Title, creds)

        if info is not None:
            refs = formatRefs(info['formatedRef'])
            return info, refs

    except:
        return None, None

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

    if len(ref1) < 10:
        return ['', '']

    return [ref1, ref2]