from io import BytesIO
import base64
import autolens as al
import numpy as np
from PIL import Image

def create_lens(redshift=0.5, einstein_radius=1.0, centre=(0.0,0.0), ell_comps=(0.0,0.0), intensity=0, effective_radius=1.0, sersic_index=1.0) -> al.Galaxy:
    return al.Galaxy(
        redshift=redshift,
        bulge=al.lp.Sersic(
            centre=centre,
            ell_comps=ell_comps,
            intensity=intensity,
            effective_radius=effective_radius,
            sersic_index=sersic_index,
        ),
        mass=al.mp.Isothermal(
            centre=centre, einstein_radius=einstein_radius, ell_comps=ell_comps
        ),
    )

def update_lens(lens: al.Galaxy, einstein_radius, centre, ell_comps, intensity, effective_radius, sersic_index, redshift=0.5):
    lens.redshift = redshift
    lens.bulge.centre = centre
    lens.bulge.ell_comps=ell_comps
    lens.bulge.intensity=intensity
    lens.bulge.effective_radius=effective_radius
    lens.bulge.sersic_index=sersic_index
    lens.mass.centre = centre
    lens.mass.einstein_radius = einstein_radius
    lens.mass.ell_comps=ell_comps


def create_source(redshift=1.0, centre=(0.0,0.0), ell_comps=(0.0,0.0), intensity=1.0, effective_radius=1.0, sersic_index=1.0) -> al.Galaxy:
    return al.Galaxy(
        redshift=redshift,
        bulge=al.lp.Sersic(
            centre=centre,
            ell_comps=ell_comps,
            intensity=intensity,
            effective_radius=effective_radius,
            sersic_index=sersic_index,
        ),
    )

def update_source(source :al.Galaxy, centre, ell_comps, intensity, effective_radius, sersic_index, redshift=1.0):
    source.redshift = redshift
    source.bulge.centre = centre
    source.bulge.ell_comps=ell_comps
    source.bulge.intensity=intensity
    source.bulge.effective_radius=effective_radius
    source.bulge.sersic_index=sersic_index

def create_grid(shape, scale = None):
    if (not scale):
        scale = 10 / shape
    return al.Grid2D.uniform(
        shape_native=(shape, shape), 
        pixel_scales=scale
    )

def update_grid(grid: al.Grid2D, shape):
    scale = 10 / shape
    grid.shape_native = (shape, shape)
    grid.pixel_scales=scale

def create_psf(grid: al.Grid2D):
    return al.Kernel2D.from_gaussian(
        shape_native=(21, 21), 
        sigma=0.1, 
        pixel_scales=grid.pixel_scales
    )

def simulate_conditions(psf, background_sky=100, exposure=720):
    return al.SimulatorImaging(
        exposure_time=exposure, 
        psf=psf, 
        background_sky_level=background_sky, 
        add_poisson_noise=True, 
        noise_seed=-1
    )

def simulate(grid, lens_galaxy, source_galaxy, simulator, shape=100):

    tracer = al.Tracer.from_galaxies(
        galaxies=[lens_galaxy, source_galaxy]
    )

    dataset = simulator.via_tracer_from(tracer=tracer, grid=grid)

    data = np.array(dataset.data)

    # Choose the lower and upper percentiles for normalization
    lower_percentile = 1
    upper_percentile = 95

    # Calculate the lower and upper limits for normalization
    lower_limit = np.percentile(data, lower_percentile)
    upper_limit = np.percentile(data, upper_percentile)

    # Clip and normalize the data to the 0-255 range
    normalized_data = np.clip(data, lower_limit, upper_limit)
    normalized_data = ((normalized_data - lower_limit) / (upper_limit - lower_limit) * 255).astype(np.uint8)

    normalized_data = normalized_data.reshape(shape,shape)

    return Image.fromarray(normalized_data).convert('L')


def pil_to_b64(im, enc_format="png", **kwargs):
    buff = BytesIO()
    im.save(buff, format=enc_format, **kwargs)
    encoded = base64.b64encode(buff.getvalue()).decode("utf-8")

    return encoded