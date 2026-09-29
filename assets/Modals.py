import dash_mantine_components as dmc
from dash import html, dcc

keyModal = dmc.Modal(
    title=dmc.Text("Key", style={"fontSize": "24px"}),
    id="helpModal",
    centered=True,
    size='850px',
    children=[dmc.Group([
        dmc.Stack([
            dmc.Paper([
                dmc.Stack([
                    html.Label('Shape', style={"fontSize": "30px"}),
                    dmc.SimpleGrid([
                        dmc.Stack([html.Label('●', style={"fontSize": "75px"}), html.Label('Paper', style={"fontSize": "20px"})]),
                        dmc.Stack([html.Label('⯃', style={"fontSize": "75px"}), html.Label('Review', style={"fontSize": "20px"})]),
                        dmc.Stack([html.Label('◆', style={"fontSize": "75px"}), html.Label('Textbook', style={"fontSize": "20px"})]),
                        dmc.Stack([html.Label('⬟', style={"fontSize": "75px"}), html.Label('Preprint', style={"fontSize": "20px"})]),
                        dmc.Stack([html.Label('⬢', style={"fontSize": "75px"}), html.Label('Thesis', style={"fontSize": "20px"})]),
                        dmc.Stack([html.Label('■', style={"fontSize": "75px"}), html.Label('Other', style={"fontSize": "20px"})]),
                    ],
                    cols=3,
                    spacing="xs",
                    verticalSpacing="xs"
                    )
                ]),
            ],
            radius="md",
            p="sm",
            shadow="sm",
            withBorder=True,
            ),
            dmc.Paper([
                dmc.Stack([
                    html.Label('Size', style={"fontSize": "30px"}),
                    dmc.Group([
                        html.Label('Least Refs', style={'width': '100px', "fontSize": "20px", 'padding': 20}),
                        html.Label('●', style={"fontSize": "30px"}),
                        html.Label('●', style={"fontSize": "40px"}),
                        html.Label('●', style={"fontSize": "50px"}),
                        html.Label('●', style={"fontSize": "60px"}),
                        html.Label('●', style={"fontSize": "70px"}),
                        html.Label('Most Refs', style={'width': '100px', "fontSize": "20px", 'padding': 20})
                    ],
                    )
            ])
            ],
            radius="md",
            p="sm",
            shadow="sm",
            withBorder=True,
            ),
        ]),
        dmc.Paper([
            dmc.Stack([
                html.Label('Colour', style={"fontSize": "30px"}),
                html.Label('Oldest'),
                html.Div(children=[],
                  style={'background': 'linear-gradient(0deg,rgba(0, 153, 255, 1) 0%, rgba(255, 0, 47, 1) 100%)',
                         'height': '92%', 'minWidth': '10vh', 'display': 'flex', 'alignItems': 'center'}),
                html.Label('Newest')],
            align="stretch",
            style={'height': '100%'}
            )
        ],
        radius="md",
        p="sm",
        shadow="sm",
        withBorder=True,
        ),
        ],
        align="stretch",
        justify="space-around"
    )],
    style={'textAlign': 'center'}
)

texModal = dmc.Modal(
    title=dmc.Text("Bibtex", style={"fontSize": "24px"}),
    id="texModal",
    centered=True,
    size='850px',
    children=[
        html.P('test', id='texMessage', style={'textAlign': 'left', 'width': '100%'}),
        dmc.Button('Copy', id='copy', n_clicks=0, style={'width': '25%'})
    ])

refModal = dmc.Modal(
    title=dmc.Text("References", style={"fontSize": "24px"}),
    id="refModal",
    centered=True,
    size='850px',
    children=[
        dcc.Textarea('test', id='RefMessage', style={'textAlign': 'left', 'width': '100%', 'height': '50vh'}, readOnly=True)
    ])

errorModal = dmc.Modal(
    title=dmc.Text("⚠️ Data Validation Error", style={"fontSize": "24px"}),
    id='errorModal',
    centered=True,
    children=[dmc.Text(id='errMessage')]
)