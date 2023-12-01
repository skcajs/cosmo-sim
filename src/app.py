from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import plotly.express as px
import components.params as params 
import components.simulation_settings as sim
import utils

app = Dash(__name__, assets_folder="../assets", external_stylesheets=[dbc.themes.LUX])
server = app.server

shape = 100
scale = 5 / shape

grid = utils.create_grid(shape=shape, scale=scale)
psf = utils.create_psf(grid=grid, psf='gaussian')
simulator = utils.simulate_conditions(psf=psf, background_sky=100, exposure=720.0)
lens_galaxy = utils.create_lens()
source_galaxy = utils.create_source()

img = utils.simulate(grid, lens_galaxy, source_galaxy, simulator, shape)
im_enc = utils.pil_to_b64(img)



app.layout = html.Div([
    html.Div([
        dmc.Grid(
            children=[
                dmc.Col(dmc.ScrollArea([
                    html.H3(children='Lensing Settings', style={'textAlign':'center'}),
                    params.lens(),
                    params.source()
                ], style={'height': '94vh', 'top':'32px'}), span=3),
                dmc.Col([
                    html.Br(),
                    html.H1(children='CosmoSim', style={'textAlign':'center'}),
                    html.Div(className="app-figure", id="output")], span=6),
                dmc.Col(
                    dmc.ScrollArea([
                    html.H3(children='Image Settings', style={'textAlign':'center'}),
                    sim.image(),
                    sim.noise()
                ], style={'height': '94vh', 'top':'32px'}), span=3
                ),
            ],
            gutter="xl",
            style={'width': '100%'}
        ),
    ], style={'paddingLeft': '32px', 'paddingRight': '32px'}),
])

@callback(
    Output('output', 'children'),
    Input('einstein_radius', 'value'),
    Input('redshift_lens', 'value'),
    Input('centre_lens_x', 'value'),
    Input('centre_lens_y', 'value'),
    Input('ell_comps_lens_x', 'value'),
    Input('ell_comps_lens_y', 'value'),
    Input('ell_comps_lens_light_x', 'value'),
    Input('ell_comps_lens_light_y', 'value'),
    Input('intensity_lens', 'value'),
    Input('effective_radius_lens', 'value'),
    Input('sersic_index_lens', 'value'),
    Input('redshift_source', 'value'),
    Input('centre_source_x', 'value'),
    Input('centre_source_y', 'value'),
    Input('ell_comps_source_x', 'value'),
    Input('ell_comps_source_y', 'value'),
    Input('intensity_source', 'value'),
    Input('effective_radius_source', 'value'),
    Input('sersic_index_source', 'value'),
    Input('resolution', 'value'),
    Input('scale', 'value'),
    Input('colour', 'value'),
    Input('psf', 'value'),
    Input('noise', 'value'),
    Input('exposure', 'value')
)
def update_graph(einstein_radius, redshift_lens, centre_lens_x, centre_lens_y, ell_comps_lens_x, ell_comps_lens_y, ell_comps_lens_light_x, ell_comps_lens_light_y, intensity_lens, effective_radius_lens, sersic_index_lens,
                 redshift_source, centre_source_x, centre_source_y, ell_comps_source_x, ell_comps_source_y, intensity_source, effective_radius_source, sersic_index_source,
                 resolution, scalef, colour, psf, noise, exposure):
        
        scale = (10 / resolution) * scalef

        grid = utils.create_grid(shape=resolution, scale=scalef)
        psf = utils.create_psf(grid=grid, psf=psf)
        simulator = utils.simulate_conditions(psf=psf, background_sky=noise, exposure=exposure)

        utils.update_lens(lens_galaxy,
            redshift=redshift_lens,
            einstein_radius=einstein_radius,
            centre=(centre_lens_x,centre_lens_y),
            ell_comps_mass=(ell_comps_lens_x, ell_comps_lens_y),
            ell_comps_light=(ell_comps_lens_light_x, ell_comps_lens_light_y),
            intensity=intensity_lens,
            effective_radius=effective_radius_lens,
            sersic_index=sersic_index_lens
        )

        utils.update_source(source_galaxy, 
            redshift=redshift_source,
            centre=(centre_source_x,centre_source_y),
            ell_comps=(ell_comps_source_x, ell_comps_source_y),
            intensity=intensity_source,
            effective_radius=effective_radius_source,
            sersic_index=sersic_index_source
        )

        im = utils.simulate(grid, lens_galaxy, source_galaxy, simulator, resolution)
        fig = px.imshow(im, color_continuous_scale=colour, aspect="equal", height=800)
        fig.update_layout(coloraxis_showscale=False)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        return dcc.Graph(figure=fig, config={'staticPlot': True, 'responsive': True})

if __name__ == '__main__':
    app.run(debug=True)