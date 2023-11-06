from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from simulator.galaxy import create_lens, create_source, update_lens, update_source
from simulator.simulate import simulate
import autolens as al
from utils import  pil_to_b64

shape = 100

grid = al.Grid2D.uniform(
    shape_native=(shape, shape), 
    pixel_scales=0.1
)

psf = al.Kernel2D.from_gaussian(
    shape_native=(21, 21), 
    sigma=0.1, 
    pixel_scales=grid.pixel_scales
)

simulator = al.SimulatorImaging(
    exposure_time=720.0, 
    psf=psf, 
    background_sky_level=100, 
    add_poisson_noise=True, 
    noise_seed=-1
)

lens_galaxy = create_lens(
)

source_galaxy = create_source(
)

im = simulate(grid, lens_galaxy, source_galaxy, simulator)
im_enc = pil_to_b64(im)

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div([
    html.Br(),
    html.H1(children='CosmoSim', style={'textAlign':'center'}),
    html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H1(children='Lens Params', style={'textAlign':'center'}),
                        html.Br(),
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
                    ], style={'padding':'32px'}),
                ),
                dbc.Col(html.Div(id="output")),
                dbc.Col(
                    html.Div([
                        html.H1(children='Source Params', style={'textAlign':'center'}),
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
                    ], style={'padding':'32px'}),
                ),
            ]
        ),
    ]),
])

@callback(
    Output('output', 'children'),
    Input('einstein_radius', 'value'),
    Input('centre_lens_x', 'value'),
    Input('centre_lens_y', 'value'),
    Input('ell_comps_lens_x', 'value'),
    Input('ell_comps_lens_y', 'value'),
    Input('intensity_lens', 'value'),
    Input('effective_radius_lens', 'value'),
    Input('sersic_index_lens', 'value'),
    Input('centre_source_x', 'value'),
    Input('centre_source_y', 'value'),
    Input('ell_comps_source_x', 'value'),
    Input('ell_comps_source_y', 'value'),
    Input('intensity_source', 'value'),
    Input('effective_radius_source', 'value'),
    Input('sersic_index_source', 'value')
)
def update_graph(einstein_radius, centre_lens_x, centre_lens_y, ell_comps_lens_x, ell_comps_lens_y, intensity_lens, effective_radius_lens, sersic_index_lens,
                 centre_source_x, centre_source_y, ell_comps_source_x, ell_comps_source_y, intensity_source, effective_radius_source, sersic_index_source):

        update_lens(lens_galaxy, 
            einstein_radius=einstein_radius,
            centre=(centre_lens_x,centre_lens_y),
            ell_comps=(ell_comps_lens_x, ell_comps_lens_y),
            intensity=intensity_lens,
            effective_radius=effective_radius_lens,
            sersic_index=sersic_index_lens
        )

        update_source(source_galaxy, 
            centre=(centre_source_x,centre_source_y),
            ell_comps=(ell_comps_source_x, ell_comps_source_y),
            intensity=intensity_source,
            effective_radius=effective_radius_source,
            sersic_index=sersic_index_source
        )

        im = simulate(grid, lens_galaxy, source_galaxy, simulator)
        fig = px.imshow(im, color_continuous_scale="gray", width=800, height=800)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run(debug=True)