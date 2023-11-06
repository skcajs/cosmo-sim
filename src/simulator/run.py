from simulate import simulate
import autolens as al
from galaxy import create_lens, create_source, update_lens, update_source
import numpy as np
from pathlib import Path



if __name__ == "__main__":
    Path("data/images").mkdir(parents=True, exist_ok=True)
    # lens_galaxy = create_lens(
    #     redshift=0.5, 
    #     einstein_radius=2.8, 
    #     ell_comps=(0.17647, 0.0), 
    #     intensity=2.3, 
    #     effective_radius=2.5, 
    #     sersic_index=1.5
    # )

    # source_galaxy = create_source(
    #     redshift=1.0,
    #     ell_comps=(-0.1, 0.111111), 
    #     intensity=1.0, 
    #     effective_radius=1.0, 
    #     sersic_index=2.5
    # )

    shape = 100
    
    grid = al.Grid2D.uniform(
        shape_native=(shape, shape), 
        pixel_scales=0.05
    )

    psf = al.Kernel2D.from_gaussian(
        shape_native=(21, 21), 
        sigma=0.1, 
        pixel_scales=grid.pixel_scales
    )

    simulator = al.SimulatorImaging(
        exposure_time=720.0, 
        psf=psf, 
        background_sky_level=1000, 
        add_poisson_noise=True, 
        noise_seed=-1
    )


    lens_galaxy = create_lens(
    )

    source_galaxy = create_source(
    )

    for i in range(20000):

        update_lens(lens_galaxy, 
            einstein_radius=np.random.uniform(0.5, 3.0),
            centre=(np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)),
            ell_comps=(np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5)),
            intensity=(np.random.uniform(0,2)),
            effective_radius=(np.random.uniform(0,2)),
            sersic_index=(1.0)
        )

        update_source(source_galaxy, 
            centre=(np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0)),
            ell_comps=(np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1)),
            intensity=(np.random.uniform(0,2)),
            effective_radius=(np.random.uniform(0,2)),
            sersic_index=(1.5)
        )

        simulate(grid, lens_galaxy, source_galaxy, psf, simulator)