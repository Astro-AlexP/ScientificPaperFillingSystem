import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from Network_calculator import create_Graph

dash.register_page(__name__, path="/Graphpage", name="Network Graph Visualizer")

data = {'Title': ['Astrophysical model selection in gravitational wave astronomy', 'On mass distribution of coalescing black holes', 'An introduction to Bayesian inference in gravitational-wave astronomy: Parameter estimation, model selection, and hierarchical models'],
        'Authors': ['Matthew R. Adams and Neil J. Cornish', '''A.D. Dolgov,a,b A.G. Kuranov,c N.A. Mitichkin,d S. Porey,a K.A. Postnov,a,b,c,1 O.S. Sazhinac and I.V. Simkine''', 'Eric Thrane and Colm Talbot'],
        'Summary': ['''Theoretical studies in gravitational wave astronomy have mostly focused on the information that can be extracted from individual detections, such as the mass of a binary system and its location in space. Here we consider how the information from multiple detections can be used to constrain astrophysical population models. This seemingly simple problem is made challenging by the high dimensionality and high degree of correlation in the parameter spaces that describe the signals, and by the complexity of the astrophysical models, which can also depend on a large number of parameters, some of which might not be directly constrained by the observations. We present a method for constraining population models using a hierarchical Bayesian modeling approach which simultaneously infers the source parameters and population model and provides the joint probability distributions for both. We illustrate this approach by considering the constraints that can be placed on population models for galactic white dwarf binaries using a future space-based gravitational wave detector. We find that a mission that is able to resolve 5000 of the shortest period binaries will be able to constrain the population model parameters, including the chirp mass distribution and a characteristic galaxy disk radius to within a few percent. This compares favorably to existing bounds, where electromagnetic observations of stars in the galaxy constrain disk radii to within 20%''',
                    '''Available data on the chirp mass distribution of the coalescing black hole binaries in O1-O3 LIGO/Virgo runs are analyzed and compared statistically with the distribution calculated under the assumption that these black holes are primordial with a log-normal mass spectrum. The theoretically calculated chirp mass distribution with the inferred best acceptable mass spectrum parameters, M0 = 17M and γ = 0.9, perfectly describes the data. The value of M0 very well agrees with the theoretically expected one. On the opposite, the chirp mass distribution of black hole binaries originated from massive binary star evolution requires additional model adjustments to reproduce the observed chirp mass distribution.''',
                    '''This is an introduction to Bayesian inference with a focus on hierarchical models and hyper-parameters. We write primarily for an audience of Bayesian novices, but we hope to provide useful insights for seasoned veterans as well. Examples are drawn from gravitational-wave astronomy, though we endeavour for the presentation to be understandable to a broader audience. We begin with a review of the fundamentals: likelihoods, priors, and posteriors. Next, we discuss Bayesian evidence, Bayes factors, odds ratios, and model selection. From there, we describe how posteriors are estimated using samplers such as Markov Chain Monte Carlo algorithms and nested sampling. Finally, we generalise the formalism to discuss hyper-parameters and hierarchical models. We include extensive appendices discussing the creation of credible intervals, Gaussian noise, explicit marginalisation, posterior predictive distributions, and selection effects.'''],
        'Keywords': ['test1, test2, test3, test4, test5, test6', 'test1, test2, test3, test4, test5, test6', 'test1, test2, test3, test4, test5, test6'],
        'id': [0, 1, 2]}
df = pd.DataFrame(data)

edges = [(0, 1), (0, 2)]

fig = create_Graph(df, edges)


layout = [
    #html.Div(children=dcc.Dropdown(['test1', 'test2', 'test3'], 'test'), style={'textAlign': 'center', 'fontSize': 20}),

    html.Div([
        html.Div(children=[
            dcc.Graph(figure=fig, id='Graph', style={'height': '85vh'}),
        ], style={'padding': 10, 'flex': '3', 'minWidth': '0', 'border': '2px solid black', 'height': '85vh'}),

        html.Div(children=[
            html.Div(children=[html.Label('Null', id='Title')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '10vh'}),
            html.Div(children=[html.Label('Null', id='Authors')], style={'textAlign': 'center', 'padding': 10, 'flex': 1, 'height': '5vh'}),
            html.Div(children=[html.Label('Null', id='Keywords')], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 10, 'flex': 1, 'border': '5px solid gray', 'height': '4vh'}),
            html.Div(children=[html.Label('Null', id='Summary')], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 10, 'flex': 1, 'border': '5px solid gray', 'height': '45vh'}),
            html.Div(children=[dcc.Button('Full Paper', id='PDF-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '3vh'}),
            html.Div(children=[dcc.Button('Bibtex', id='Bibtex-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '3vh'}),
            html.Div(children=[dcc.Button('Reference List', id='Reference-button', n_clicks=0)], style={'textAlign': 'center', 'fontSize': 'clamp(8px, 1.7vh, 30px)', 'padding': 3, 'flex': 1, 'height': '3vh'})
        ], style={'padding': 10, 'flex': '2', 'minWidth': '0', 'border': '2px solid black'})
    ], style={'display': 'flex', 'flexDirection': 'row',})]


@callback(
    Output('Title', 'children'),
    Output('Authors', 'children'),
    Output('Keywords', 'children'),
    Output('Summary', 'children'),
    Input('Graph', 'clickData'))
def update_paper(clickData):
    if clickData is not None:
        data = clickData['points'][0]['customdata']
        return data[0], data[1], data[3], data[2]

    return 'Null', 'Null', 'Null', 'Null'

@callback(
    Output('Title', 'style'),
    Input('Graph', 'clickData')
)
def update_Title_font_size(clickData):
    if clickData is not None:
        TitleLen = len(clickData['points'][0]['customdata'][0])

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
    Input('Graph', 'clickData')
)
def update_Authors_font_size(clickData):
    if clickData is not None:
        TitleLen = len(clickData['points'][0]['customdata'][1])

        size = 10 * (TitleLen**(-0.08))-5
        height = 0.8

        return {
            'fontSize': f'clamp(10px, {size}vh, 32px)',
            'lineHeight': f'{height}',
            'overflowWrap': 'break-word'  # Ensures long words split instead of clipping
        }
    return {'fontSize': 'clamp(10px, 2.4vh, 32px)', 'lineHeight': '0.8'}