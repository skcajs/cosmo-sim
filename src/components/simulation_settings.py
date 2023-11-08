from dash import html, dcc
import dash_mantine_components as dmc

def image():
    return html.Div([
        html.Br(),
        html.Div([
            "Image resolution",
            dcc.Slider(50, 400, value=100, id='resolution'),
        ]),
        html.Div([
            "Pixel scale",
            dcc.Slider(0.5, 2.5, value=1, id='scale'),
        ]),
        html.Div([
            "Colour scale",
            dmc.Select(
                placeholder="Select one",
                id="colour",
                value="gray",
                data=[
                    {"value": "gray", "label": "Grey"},
                    {"value": "Viridis", "label": "Viridis"},
                    {"value": "Magma", "label": "Magma"},
                    {"value": "Jet", "label": "Jet"},
                    {"value": "ice", "label": "Ice"},
                    {"value": "matter", "label": "Matter"},
                ],
                style={"marginBottom": 10, "paddingLeft": 16, "paddingRight": 16},
            ),
        ])                 
    ], style={'padding':'32px', 'textAlign': 'right'})