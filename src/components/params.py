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
            dmc.Slider(min=0, max=3.5, step=0.01, value=1.6, id='einstein_radius'),
        ]),
        html.Div([
            "Reshift",
            dmc.Slider(min=0.4, max=0.6, step=0.01, value=0.5, id='redshift_lens'),
        ]),
        html.Div([
            "Centre (lens mass x)",
            dmc.Slider(min=-1, max=1, step=0.01, value=0, id='centre_lens_x'),
        ]),
        html.Div([
            "Centre (lens mass y)",
            dmc.Slider(min=-1, max=1, step=0.01, value=0, id='centre_lens_y'),
        ]),
        html.Div([
            "Ell Comps (lens mass x)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_lens_x'),
        ]),
        html.Div([
            "Ell Comps (lens mass y)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_lens_y'),
        ]),
        html.Div([
            "Ell Comps (lens light x)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_lens_light_x'),
        ]),
        html.Div([
            "Ell Comps (lens light y)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_lens_light_y'),
        ]),
        html.Div([
            "Intensity (lens light)",
            dmc.Slider(min=0, max=5, step=0.01, value=0, id='intensity_lens'),
        ]),
        html.Div([
            "Effective radius (lens light)",
            dmc.Slider(min=0, max=5, step=0.01, value=0, id='effective_radius_lens'),
        ]),
        html.Div([
            "serseic index (lens light)",
            dmc.Slider(min=1, max=5, step=0.01, value=1.0, id='sersic_index_lens'),
        ]),                     
    ], style={'padding':'32px'})

def source():
    return html.Div([
        html.H4(children='Source Params'),
        html.Br(),
        html.Div([
            "Reshift",
            dmc.Slider(min=1.5, max=4, step=0.01, value=1.5, id='redshift_source'),
        ]),
        html.Div([
            "Centre (source light x)",
            dmc.Slider(min=-1, max=1, step=0.01, value=0, id='centre_source_x'),
        ]),
        html.Div([
            "Centre (source light y)",
            dmc.Slider(min=-1, max=1, step=0.01, value=0, id='centre_source_y'),
        ]),
        html.Div([
            "Ell Comps (source light y)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_source_x'),
        ]),
        html.Div([
            "Ell Comps (lens mass y)",
            dmc.Slider(min=-0.4, max=0.4, step=0.01, value=0, id='ell_comps_source_y'),
        ]),
        html.Div([
            "Intensity (source)",
            dmc.Slider(min=0, max=5, step=0.01, value=1, id='intensity_source'),
        ]),
        html.Div([
            "Effective radius (source)",
            dmc.Slider(min=0, max=5, step=0.01, value=1, id='effective_radius_source'),
        ]),
        html.Div([
            "Sersic index (source)",
            dmc.Slider(min=0.5, max=5, step=0.01, value=1.5, id='sersic_index_source'),
        ]),                       
    ], style={'padding':'32px'})