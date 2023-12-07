from simulator.simulate import simulate
import time
import autolens as al
from utils import create_lens, create_source, update_lens, update_source, create_psf, point_in_caustics
import numpy as np
from pathlib import Path
from random import choice
from string import ascii_lowercase, digits
import csv

if __name__ == "__main__":
    size = 100
    filepath = 'data/{0}_{1}/'.format(time.strftime("%Y%m%d%H%M%S"), size)
    Path("{}/images".format(filepath)).mkdir(parents=True, exist_ok=True)

    shape = 100
    # scale = 10 / shape
    scale = 0.05
    
    grid = al.Grid2D.uniform(
        shape_native=(shape, shape), 
        pixel_scales=scale
    )

    # psf = create_psf(grid, psf='./data/psf/slacs/F814W_psf.fits')

    psf = create_psf(grid, psf='gaussian')

    simulator = al.SimulatorImaging(
        exposure_time=720.0, 
        psf=psf, 
        background_sky_level=800, 
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
        
        # lens_writer.writerow([
        #     'name', 'r_ein', 'rdsf_l' ,'r_eff_l', 'x_l', 'y_l', 'ellx_l', 'elly_l', 'ellxl_l', 'ellyl_l', 'int_l', 
        #     'rdsf_s', 'r_eff_s', 'x_s', 'y_s', 'ellx_s', 'elly_s', 'int_s', 'si_s'])
        
        lens_writer.writerow([
            'name', 'r_ein', 'x_l', 'y_l', 'ellx_l', 'elly_l', 'x_s', 'y_s'])


        for i in range(size):

            # einstein_radius=np.random.uniform(0.8, 2.0)
            # redshift_lens=np.random.uniform(0.1, 0.4)
            # centre_lens=(np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5))
            # ell_comps_lens=(np.random.uniform(-0.4, 0.4), np.random.uniform(-0.4, 0.4))
            # ell_comps_lens_light=(0, 0)
            # intensity_lens=0
            # effective_radius_lens=0

            # redshift_source=np.random.uniform(0.5, 1.2)
            
            # ell_comps_source=(np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1))
            # intensity_source=np.random.uniform(0.1,4)
            # effective_radius_source=np.random.uniform(0.1,1)
            # sersic_index_source=np.random.uniform(1, 5)


            einstein_radius=np.random.uniform(0.8, 2.0)
            redshift_lens=np.random.uniform(0.1, 0.4)
            centre_lens=(np.random.uniform(-0.5, 0.5), np.random.uniform(-0.5, 0.5))
            ell_comps_lens=(np.random.uniform(-0.4, 0.4), np.random.uniform(-0.4, 0.4))
            ell_comps_lens_light=(0, 0)
            intensity_lens=0
            effective_radius_lens=0

            redshift_source=np.random.uniform(0.5, 1.2)
            ell_comps_source=(np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1))
            intensity_source=np.random.uniform(0.5,1)
            effective_radius_source=np.random.uniform(0.5,1)
            sersic_index_source=np.random.uniform(1.5, 2)

            update_lens(lens_galaxy, 
                einstein_radius=einstein_radius,
                centre=centre_lens,
                ell_comps_mass=ell_comps_lens,
                ell_comps_light=ell_comps_lens_light,
                intensity=intensity_lens,
                effective_radius=effective_radius_lens,
                sersic_index=1,
                redshift=redshift_lens
            )

            centre_source=point_in_caustics(lens_galaxy=lens_galaxy, grid=grid)

            update_source(source_galaxy, 
                centre=centre_source,
                ell_comps=ell_comps_source,
                intensity=intensity_source,
                effective_radius=effective_radius_source,
                sersic_index=sersic_index_source,
                redshift=redshift_source
            )

            im = simulate(grid, lens_galaxy, source_galaxy, simulator)
            filename = '{}.png'.format(''.join(choice(ascii_lowercase + digits) for _ in range(6)))
            im.save('{0}/images/{1}'.format(filepath, filename))

            # lens_writer.writerow([filename , einstein_radius, redshift_lens, effective_radius_lens, centre_lens[0], centre_lens[1], 
            #                     ell_comps_lens[0], ell_comps_lens[1], ell_comps_lens_light[0], ell_comps_lens_light[1], intensity_lens, redshift_source, effective_radius_source, 
            #                     centre_source[0], centre_source[1], ell_comps_source[0], ell_comps_source[1], intensity_source, sersic_index_source])
            
            lens_writer.writerow([filename , einstein_radius, centre_lens[0], centre_lens[1], ell_comps_lens[0], ell_comps_lens[1], centre_source[0], centre_source[1]])