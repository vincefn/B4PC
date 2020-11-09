#-----------------------------------------------------------------------------#
# Copyright (c) 2020 Institute of High Energy Physics Chinese Academy of 
#                    Science
#-----------------------------------------------------------------------------#

__authors__  = "Han Xu - HEPS Hard X-ray Scattering Beamline (B4)"
__date__     = "Date : 10.07.2020"
__version__  = "Alpha-2.0"


"""
slit: The simulation of secondary source slit. 

Functions: none.
           
Classes  : none.
           
"""

#-----------------------------------------------------------------------------#
# libraries

import elements 
import propagate
import pickle
import numpy as np

#-----------------------------------------------------------------------------#
# classes

source = elements.LightSource(
    source_count = 2079,
    wave_length = 1e-4,
    source_sigma = [9.5, 3.1],
    optic_planesize = [38, 13],
    optic_pixelsize = [0.5, 0.5],
    )
source.gauss_source()

ideal_lens = elements.OpticElements(
    source_class = source,
    name = "lens",
    order = 1,
    optic_location = 40e6,
    optic_planesize = [60, 60],
    optic_pixelsize = [5.0, 5.0],
    optic_planecount = 14641,
    optic_focus = 29.3e6
    )

slit = elements.OpticElements(
    source_class = source,
    name = "slit",
    order = 2,
    optic_location = 69.3e6,
    optic_planesize = [10, 13],
    optic_pixelsize = [0.5, 0.5],
    optic_planecount = 567,
    )

if __name__ == '__main__':
    
    propagate.source_spread(source, ideal_lens)
    propagate.lens(source, ideal_lens, 1)
    propagate.kirchhoff_integral(ideal_lens, slit)
    
    slit.save() 

