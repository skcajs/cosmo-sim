import autolens as al

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