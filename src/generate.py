from simulator.simulate import simulate
import time
import autolens as al
from utils import create_lens, create_source, update_lens, update_source
import numpy as np
from pathlib import Path
from random import choice
from string import ascii_lowercase, digits
import csv

if __name__ == "__main__":
    size = 1000000
    filepath = 'data/{0}_{1}/'.format(time.strftime("%Y%m%d%H%M%S"), size)
    Path("{}/images".format(filepath)).mkdir(parents=True, exist_ok=True)

    shape = 100
    scale = 10 / shape
    
    grid = al.Grid2D.uniform(
        shape_native=(shape, shape), 
        pixel_scales=scale
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

    with open('{}/labels.csv'.format(filepath), 'w', newline='') as csvfile:

        lens_writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        lens_writer.writerow([
            'name', 'r_ein', 'rdsf_l' ,'r_eff_l', 'x_l', 'y_l', 'ellx_l', 'elly_l', 'int_l', 
            'rdsf_s', 'r_eff_s', 'x_s', 'y_s', 'ellx_s', 'elly_s', 'int_s'])


        for i in range(size):
            einstein_radius=np.random.uniform(0.5, 3.0)
            redshift_lens=np.random.uniform(0.4, 0.7)
            centre_lens=(np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0))
            ell_comps_lens=(np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5))
            intensity_lens=np.random.uniform(0,2)
            effective_radius_lens=np.random.uniform(0,2)

            redshift_source=np.random.uniform(1.5, 2.5)
            centre_source=(np.random.uniform(-1.0, 1.0), np.random.uniform(-1.0, 1.0))
            ell_comps_source=(np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5))
            intensity_source=np.random.uniform(0,2)
            effective_radius_source=np.random.uniform(0,2)

            update_lens(lens_galaxy, 
                einstein_radius=einstein_radius,
                centre=centre_lens,
                ell_comps=ell_comps_lens,
                intensity=intensity_lens,
                effective_radius=effective_radius_lens,
                sersic_index=1.0,
                redshift=redshift_lens
            )

            update_source(source_galaxy, 
                centre=centre_source,
                ell_comps=ell_comps_source,
                intensity=intensity_source,
                effective_radius=effective_radius_source,
                sersic_index=1.5,
                redshift=redshift_source
            )

            im = simulate(grid, lens_galaxy, source_galaxy, simulator)
            filename = '{}.png'.format(''.join(choice(ascii_lowercase + digits) for _ in range(6)))
            im.save('{0}/images/{1}'.format(filepath, filename))

            lens_writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            lens_writer.writerow([filename , einstein_radius, redshift_lens, effective_radius_lens, centre_lens[0], centre_lens[1], 
                                ell_comps_lens[0], ell_comps_lens[1], intensity_lens, redshift_source, effective_radius_source, 
                                centre_source[0], centre_source[1], ell_comps_source[0], ell_comps_source[1], intensity_source])
    
