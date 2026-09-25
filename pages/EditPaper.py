import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from Paper_Info import fetchOpenalexDataDOI, fetchOpenalexDataTitle, getCredentials
from Database import savePaper, readDatabase, editPaper, deletePaper
from Network_calculator import makeGraph
import base64

dash.register_page(__name__, path="/EditPaper", name="Edit Paper")

layout = [
    html.Div([
            dbc.Modal(id='EditerrorModal',
                children = [
                    dbc.ModalHeader(dbc.ModalTitle("⚠️ Data Validation Error")),
                    dbc.ModalBody(id='EditerrMessage', children='test'), # Dynamic error text goes here
                ],
                is_open=False, # Hidden initially
                centered=True  # Centers it vertically on the screen!
            ),
        dcc.Store(id='EditpaperData', storage_type='session'),
        dcc.Store(id='EditfileData', storage_type='session'),
        dcc.Store(id='EditPaperID', storage_type='session'),
        html.Div(children=[
            html.Div(children=[
                html.Label('PaperID:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Dropdown(id='EditIDInput', style={'width': '75%', 'height': '75%', 'resize': 'none', 'display': 'flex'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '6vh'}),
            html.Div(children=[
                html.Label('Title:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='EditTitleInput', style={'width': '75%', 'height': '75%', 'resize': 'none', 'display': 'flex'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '6vh'}),
            html.Div(children=[
                html.Label('Authors:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='EditAuthorsInput', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('DOI:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='EditDOIInput', type='text', style={'width': '75%'}),
                html.Div(style={'width': '3%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('Keywords:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='EditKeywordsInput', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('File:', style={'fontSize': '2.5vh', 'width': '12%'}),
                html.Div(dcc.Upload(id='Editupload', accept="application/pdf", children=html.Div([
                    html.I(className="bi bi-cloud-arrow-up")],
                    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'alignItems': 'center', 'width': '100%', 'height': '100%'})),
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'width': '2%', 'boxSizing': 'border-box', 'justifyContent': 'center', 'height': '35px', 'border': '1px solid #888888', 'borderRadius': '5px', 'cursor': 'pointer'}),
                dcc.Input(id='EditfilePath', type='text', style={'width': '73%', 'height': '35px'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('Summary:', style={'fontSize': '2.5vh', 'width': '12%'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                dcc.Textarea(id='EditSummaryInput', style={'width': '95%', 'height':'100%', 'resize': 'none'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '45vh'}),
            html.Div(children=[
                html.Div(style={'width': '4.5%'}),
                dcc.Button('Clear', id='EditClear', n_clicks=0, style={'width': '27%', 'height': '100%'}),
                html.Div(style={'width': '5%'}),
                dcc.Button('Save', id='EditSave', n_clicks=0, style={'width': '27%', 'height': '100%'}),
                html.Div(style={'width': '5%'}),
                dcc.Button('Delete', id='EditDelete', n_clicks=0, style={'width': '27%', 'height': '100%'}),
                html.Div(style={'width': '4.5%'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'height': '7.5%'} )
        ], style={'display': 'flex', 'flexDirection': 'column', 'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '85vh'}),

        html.Div(children=[
            html.Div(children=[
                html.Label('References')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '10vh', 'fontSize': '4vh'}),
            html.Div(children=[
                dcc.Textarea(id='Editref1', style={'width': '45%', 'height': '150%', 'resize': 'none'}, readOnly=True), dcc.Textarea(id='Editref2', style={'width': '45%', 'height': '150%', 'resize': 'none'}, readOnly=True)],
            style={'textAlign': 'center', 'padding': 10, 'flex': 9, 'height': '45vh'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'}),
    ], style={'display': 'flex', 'flexDirection': 'row', })]

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
    Output('EditerrorModal', 'is_open'),
    Output('EditerrMessage', 'children'),
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