import dash
from dash import html, dcc, callback, Output, Input, State
import dash_mantine_components as dmc
from Database import readDatabase, editPaper, deletePaper
from Network_calculator import makeGraph
import base64

from assets import Modals

dash.register_page(__name__, path="/EditPaper", name="Edit Paper")

layout = [
    html.Div([
            Modals.errorModal,
        dcc.Store(id='EditpaperData', storage_type='session'),
        dcc.Store(id='EditfileData', storage_type='session'),
        dcc.Store(id='EditPaperID', storage_type='session'),

        dmc.Grid(
            columns=10,
            children=[
                dmc.GridCol([
                    dmc.Paper([
                        dmc.Stack([
                            dmc.Group([
                                dmc.Text('PaperID:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Dropdown(id='EditIDInput', style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Title:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='EditTitleInput', style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Authors:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='EditAuthorsInput',
                                             style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('DOI:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='EditDOIInput', style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('Keywords:', style={'fontSize': 30, 'width':'140px'}),
                                dcc.Textarea(id='EditKeywordsInput',
                                             style={'width': '75%', 'height': '30px', 'resize': 'none'})
                            ],
                                align='center',
                                justify='flex-start',
                                gap="md",
                                style={'height': '4%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Text('File:', style={'fontSize': 30, 'width':'140px'}),
                                html.Div([html.Div([dcc.Upload(id='Editupload', accept="application/pdf", children=html.Div([html.I(className="bi bi-cloud-arrow-up")],)),
                                          ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'width': '3%', 'boxSizing': 'border-box', 'justifyContent': 'center', 'height': '35px', 'border': '1px solid #888888', 'borderRadius': '5px', 'cursor': 'pointer'}),
                                    dcc.Input(id='EditfilePath', type='text', style={'width': '97%', 'height': '35px'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row','width': '75%'}),

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
                                dcc.Textarea(id='EditSummaryInput', style={'width': '95%', 'height':'100%', 'resize': 'none'}),
                            ],
                                align='center',
                                justify='center',
                                gap="md",
                                style={'height': '60%', 'width': '100%'}),
                            dmc.Group([
                                dmc.Button('Clear', id='EditClear', n_clicks=0, style={'width': '30%', 'height': '100%'}),
                                dmc.Button('Delete', id='EditDelete', n_clicks=0, style={'width': '30%', 'height': '100%'}),
                                dmc.Button('Save', id='EditSave', n_clicks=0, style={'width': '30%', 'height': '100%'}),
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
                                dcc.Textarea(id='Editref1', readOnly=True, style={'height': '100%', 'resize': 'none'}),
                                dcc.Textarea(id='Editref2', readOnly=True, style={'height': '100%', 'resize': 'none'})
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
    Output('EditTitleInput', 'value'),
    Output('EditAuthorsInput', 'value'),
    Output('EditDOIInput', 'value'),
    Output('EditKeywordsInput', 'value'),
    Output('EditSummaryInput', 'value'),
    Output('Editref1', 'value'),
    Output('Editref2', 'value'),
    Output('EditClear', 'n_clicks'),
    Output('EditSave', 'n_clicks'),
    Output('EditDelete', 'n_clicks'),
    Output('EditpaperData', 'data'),
    Output('EditfileData', 'data'),
    Output('EditPaperID', 'data'),
    Output('EditfilePath', 'value'),
    Output('errorModal', 'is_open', allow_duplicate=True),
    Output('errMessage', 'children', allow_duplicate=True),
    Output('Data', 'data', allow_duplicate=True),
    Output('Edges', 'data', allow_duplicate=True),
    Output('fig', 'data', allow_duplicate=True),
    Output('EditIDInput', 'value'),
    Output('EditIDInput', 'options'),
    Input('EditClear', 'n_clicks'),
    Input('EditSave', 'n_clicks'),
    Input('EditDelete', 'n_clicks'),
    Input('Editupload', 'filename'),
    Input('Editupload', 'contents'),
    Input('EditIDInput', 'value'),
    State('EditTitleInput', 'value'),
    State('EditAuthorsInput', 'value'),
    State('EditDOIInput', 'value'),
    State('EditfilePath', 'value'),
    State('EditKeywordsInput', 'value'),
    State('EditSummaryInput', 'value'),
    State('EditpaperData', 'data'),
    State('EditfileData', 'data'),
    State('EditPaperID', 'data'),
    State('Data', 'data'),
    State('Edges', 'data'),
    State('fig', 'data'),
    prevent_initial_call=True
)
def formControls(ClearB, Save, Delete, UploadName, UploadContent, ID, Title, Authors, DOI, filePath, Keywords, Summary, paperData, fileData, paperID, data, Edges, fig):
    IDs = []
    for i in range(len(data['Title'])):
        IDs.append(str(i + 1) + ', ' + data['Title'][i])

    if paperData is None:
        paperData = {'formatedRef': []}
        paperData['formatedRef'] = ['', '']

    if ClearB > 0:
        ClearB = 0
        return None, None, None, None, '', '', '', ClearB, Save, Delete, None, None, None, None, False, None, data, Edges, fig, ID, IDs

    if Save > 0:
        Save = 0
        try:
            editPaper(Title, DOI, Summary, Keywords, filePath, fileData, paperID)
            data, edges = readDatabase()
            fig = makeGraph(data, edges)

            IDs = []
            for i in range(len(data['Title'])):
                IDs.append(str(i + 1) + ', ' + data['Title'][i])

            return '', None, None, None, '', '', '', ClearB, Save, Delete, None, None, None, None, False, None, data, Edges, fig, ID, IDs
        except:
            refs = formatRefs(paperData['formatedRef'])
            return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], ClearB, Save, Delete, paperData, fileData, paperID, filePath, True, 'Data not entries not complete', data, Edges, fig, ID, IDs

    if Delete > 0:
        Delete = 0
        if paperID is not None:
            deletePaper(paperID)

            data, edges = readDatabase()
            fig = makeGraph(data, edges)

            IDs = []
            for i in range(len(data['Title'])):
                IDs.append(str(i + 1) + ', ' + data['Title'][i])

        return None, None, None, None, '', '', '', ClearB, Save, Delete, None, None, None, None, False, None, data, Edges, fig, ID, IDs

    if UploadName is not None:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], ClearB, Save, Delete, paperData, UploadContent, paperID, UploadName, False, data, Edges, fig, ID, IDs

    if ID is not None:
        IDnum = int(ID[0]) - 1
        refs = formatRefs(data['Refs'][IDnum])

        with open(data['Link'][IDnum], 'rb') as f:
            content_type = "application/pdf"
            fileData = base64.b64encode(f.read())
            fileData = fileData.decode("ascii")
            fileData = f"data:{content_type};base64,{fileData}"

        return data['Title'][IDnum], AuthorFormat(data['Authors'][IDnum]), data['DOI'][IDnum], KeywordFormat(data['Keywords'][IDnum]), data['Summary'][IDnum], refs[0], refs[1], ClearB, Save, Delete, paperData, fileData, IDnum + 1, data['Link'][IDnum], False, None, data, Edges, fig, ID, IDs

    else:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], ClearB, Save, Delete, paperData, fileData, paperID, filePath, False, None, data, Edges, fig, ID, IDs

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

def AuthorFormat(Authors):
    AuthorString = ''
    for i in range(len(Authors)):
        AuthorString += Authors[i]
        AuthorString += ', '

    return AuthorString[:-2]

def KeywordFormat(Keywords):
    keywordString = ''
    for keyword in Keywords:
        keywordString += keyword + ', '

    return keywordString[:-2]