from dash import html, dcc
import dash_mantine_components as dmc

def lens():
    return html.Div([
        html.H4(children='Lens Params'),
        html.Br(),
        # html.Div([
        #     "Einstein Radius",
        #     dmc.Slider(
        #         min=0, 
        #         max=3, 
        #         step=0.01,
        #         value=2.8,
        #         marks=[{"value":1},{"value":2}],
        #         id='einstein_radius'),
        # ]),
        html.Div([
            "Einstein Radius",
            dcc.Slider(0, 3, value=2.8, id='einstein_radius'),
        ]),
        html.Div([
            "Centre (lens mass x)",
            dcc.Slider(-1, 1, value=0, id='centre_lens_x'),
        ]),
        html.Div([
            "Centre (lens mass y)",
            dcc.Slider(-1, 1, value=0, id='centre_lens_y'),
        ]),
        html.Div([
            "Ell Comps (lens mass x)",
            dcc.Slider(-0.4, 0.4, value=0, id='ell_comps_lens_x'),
        ]),
        html.Div([
            "Ell Comps (lens mass y)",
            dcc.Slider(-0.4, 0.4, value=0, id='ell_comps_lens_y'),
        ]),
        html.Div([
            "Intensity (lens light)",
            dcc.Slider(0, 5, value=2, id='intensity_lens'),
        ]),
        html.Div([
            "Effective radius (lens light)",
            dcc.Slider(0, 5, value=1, id='effective_radius_lens'),
        ]),
        html.Div([
            "serseic index (lens light)",
            dcc.Slider(1, 5, value=1.0, id='sersic_index_lens'),
        ]),                     
    ], style={'padding':'32px'})

def source():
    return html.Div([
        html.H4(children='Source Params'),
        html.Br(),
        html.Div([
            "Centre (source light x)",
            dcc.Slider(-1, 1, value=0, id='centre_source_x'),
        ]),
        html.Div([
            "Centre (source light y)",
            dcc.Slider(-1, 1, value=0, id='centre_source_y'),
        ]),
        html.Div([
            "Ell Comps (source light y)",
            dcc.Slider(-0.4, 0.4, value=0, id='ell_comps_source_x'),
        ]),
        html.Div([
            "Ell Comps (lens mass y)",
            dcc.Slider(-0.4, 0.4, value=0, id='ell_comps_source_y'),
        ]),
        html.Div([
            "Intensity (source)",
            dcc.Slider(0, 5, value=1, id='intensity_source'),
        ]),
        html.Div([
            "Effective radius (source)",
            dcc.Slider(0, 5, value=1, id='effective_radius_source'),
        ]),
        html.Div([
            "Sersic index (source)",
            dcc.Slider(0.5, 5, value=1.5, id='sersic_index_source'),
        ]),                       
    ], style={'padding':'32px'})