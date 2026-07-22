import dash
from dash import html, dcc, callback, Output, Input, State, ctx
import dash_bootstrap_components as dbc
from Paper_Info import fetchOpenalexDataDOI, fetchOpenalexDataTitle, getCredentials
from Database import savePaper

import sqlite3

dash.register_page(__name__, path="/NewPaper", name="Add New Paper")


layout = [
    html.Div([
            dbc.Modal(id='errorModal',
                children = [
                    dbc.ModalHeader(dbc.ModalTitle("⚠️ Data Validation Error")),
                    dbc.ModalBody(id='errMessage', children='test'), # Dynamic error text goes here
                ],
                is_open=False, # Hidden initially
                centered=True  # Centers it vertically on the screen!
            ),
        dcc.Store(id='paperData', storage_type='session'),
        dcc.Store(id='fileData', storage_type='session'),
        html.Div(children=[
            html.Div(children=[
                html.Label('Title:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Textarea(id='TitleInput', style={'width': '75%', 'height': '150%', 'resize': 'none'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '6vh'}),
            html.Div(children=[
                html.Label('Authors:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='AuthorsInput', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('DOI:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='DOIInput', type='text', style={'width': '75%'}),
                html.Div(style={'width': '3%'}),
                dcc.Button('Search', id='Search', n_clicks=0, style={'width': '7%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('Keywords:', style={'fontSize': '2.5vh', 'width': '12%'}),
                dcc.Input(id='KeywordsInput', type='text', style={'width': '75%'})],
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('File:', style={'fontSize': '2.5vh', 'width': '12%'}),
                html.Div(dcc.Upload(id='upload', accept="application/pdf", children=html.Div([
                    html.I(className="bi bi-cloud-arrow-up")],
                    style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'center', 'alignItems': 'center', 'width': '100%', 'height': '100%'})),
                style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'width': '2%', 'boxSizing': 'border-box', 'justifyContent': 'center', 'height': '35px', 'border': '1px solid #888888', 'borderRadius': '5px', 'cursor': 'pointer'}),
                dcc.Input(id='filePath', type='text', style={'width': '73%', 'height': '35px'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                html.Label('Summary:', style={'fontSize': '2.5vh', 'width': '12%'})], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '5vh'}),
            html.Div(children=[
                dcc.Textarea(id='SummaryInput', style={'width': '95%', 'height':'100%', 'resize': 'none'})], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center', 'flexDirection': 'row', 'padding': 10, 'height': '45vh'}),
            html.Div(children=[
                html.Div(style={'width': '2.5%'}),
                dcc.Button('Clear', id='Clear', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '5%'}),
                dcc.Button('Save', id='Save', n_clicks=0, style={'width': '45%', 'height': '100%'}),
                html.Div(style={'width': '2.5%'}),
            ], style={'display': 'flex', 'alignItems': 'center', 'flexDirection': 'row', 'height': '7.5%'} )
        ], style={'display': 'flex', 'flexDirection': 'column', 'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '85vh'}),

        html.Div(children=[
            html.Div(children=[
                html.Label('References')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '10vh', 'fontSize': '4vh'}),
            html.Div(children=[
                dcc.Textarea(id='ref1', style={'width': '45%', 'height': '150%', 'resize': 'none'}), dcc.Textarea(id='ref2', style={'width': '45%', 'height': '150%', 'resize': 'none'})],
            style={'textAlign': 'center', 'padding': 10, 'flex': 9, 'height': '45vh'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'}),
    ], style={'display': 'flex', 'flexDirection': 'row', })]

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
    prevent_initial_call=True
)
def formControls(Search, ClearB, Save, UploadName, UploadContent, Title, Authors, DOI, filePath, Keywords, Summary, paperData, fileData):
    if paperData is None:
        paperData = {'formatedRef': []}
        paperData['formatedRef'] = ['', '']
    if Search > 0:
        Search = 0
        creds = getCredentials()
        info, refs = paperSearch(Title, DOI, creds)
        if info is not None and refs is not None:
            refs = formatRefs(info['formatedRef'])
            return info['Title'], info['Authors'], info['DOI'], Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, info, fileData, filePath, False, None

        else:
            refs = formatRefs(paperData['formatedRef'])
            return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, None, None, filePath, True, 'No paper found'

    if ClearB > 0:
        ClearB = 0
        return '', None, None, None, '', '', '', Search, ClearB, Save, None, None, None, None, False, None

    if Save > 0:
        Save = 0
        if Title is not None and Authors is not None and DOI is not None and filePath is not None and Keywords is not None and Summary is not None and paperData is not None:
            savePaper(Title, Authors, DOI, Keywords, Summary, filePath, paperData, fileData)
            return '', None, None, None, '', '', '', Search, ClearB, Save, None, None, None, False, None
        else:
            refs = formatRefs(paperData['formatedRef'])
            return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, fileData, filePath, True, 'Data not entries not complete'

    if UploadName is not None:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, UploadContent, UploadName, False, None

    else:
        refs = formatRefs(paperData['formatedRef'])
        return Title, Authors, DOI, Keywords, Summary, refs[0], refs[1], Search, ClearB, Save, paperData, fileData, filePath, False, None



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

    return [ref1, ref2]