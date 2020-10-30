"""The calculation of secondary source of beamline 4.

Time: 16:00 2019.12.23
Author: Han Xu
Email: xuhan@ihep.ac.cn
"""


################################################################################
# LIBARY

import elements 
import propagate
import pickle
import numpy as np

# Inializting the optical elements of beamline
source = elements.LightSource(
    source_count = 2079,
    wave_length = 1e-4,
    source_sigma = [9.5, 3.1],
    optic_planesize = [38, 13],
    optic_pixelsize = [0.5, 0.5],
    )
source.gauss_source()

crl = elements.OpticElements(
    source_class = source,
    name = "crl",
    order = 1,
    optic_location = 40e6,
    optic_planesize = [60, 60],
    optic_pixelsize = [5.0, 5.0],
    optic_planecount = 14641,
    optic_focus = 29.3e6
    )

slit = elements.OpticElements(
    source_class = source,
    name = "secsource_slit",
    order = 3,
    optic_location = 69.3e6,
    optic_planesize = [10, 13],
    optic_pixelsize = [0.5, 0.5],
    optic_planecount = 567,
    )

sample = elements.OpticElements(
        source_class = source,
        name = "test_sample",
        order = 4,
        optic_location = 72.0e6,
        optic_planesize = [64, 64],
        optic_pixelsize = [0.1575, 0.1575],
        optic_planecount = 16641)


if __name__ == '__main__':
    
    propagate.source_spread(source, crl)
    propagate.lens(source, crl, 1)
    propagate.kirch_integral(crl, slit)
    propagate.kirch_integral(slit, sample)
    sample.save() 
