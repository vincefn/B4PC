#-----------------------------------------------------------------------------#
# Copyright (c) 2020 Institute of High Energy Physics Chinese Academy of 
#                    Science
#-----------------------------------------------------------------------------#

__authors__  = "Han Xu - HEPS Hard X-ray Scattering Beamline (B4)"
__date__     = "Date : 10.07.2020"
__version__  = "Alpha-2.0"


"""
sample_plane: The simulation of intensity at sample plane. 

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

sample_plane = elements.OpticElements(
    source_class = source,
    name = "sample_plane",
    order = 3,
    optic_location = 72.0e6,
    optic_planesize = [64, 64],
    optic_pixelsize = [0.1575, 0.1575],
    optic_planecount = 16641
    )


if __name__ == '__main__':
    
    slit = pickle.load(open("slit.pkl", 'rb'))
    propagate.kirchhoff_integral(slit, sample_plane)    
    sample_plane.save() 