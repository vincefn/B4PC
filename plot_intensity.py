#-----------------------------------------------------------------------------#
# Copyright (c) 2020 Institute of High Energy Physics Chinese Academy of 
#                    Science
#-----------------------------------------------------------------------------#

__authors__  = "Han Xu - HEPS Hard X-ray Scattering Beamline (B4)"
__date__     = "Date : 10.07.2020"
__version__  = "Alpha-2.0"


"""
plot: Plot the result. 

paper: "A Wave Optics Model for the Effect of Partial Coherence on Coherent 
        Diffractive Imaging"
        
fig1. the secondary source. Figure.2 of paper.
fig2. the intensity at the sample plane. Figure.7a of paper. 
    
Functions: none.
           
Classes  : none.    
"""

#-----------------------------------------------------------------------------#
# libaries

import pickle
import matplotlib.pyplot as plt
import numpy as np

#-----------------------------------------------------------------------------#
# plot secondary source

secondary_source = pickle.load(open("secondary_source_intensity.pkl", 'rb'))

x = np.linspace(-30*0.5, 30*0.5, 61)
y = np.linspace(-15*0.5, 15*0.5, 31)

plt.figure(figsize = (8, 4))
plt.pcolor(x, y, secondary_source, cmap = 'jet') 
plt.colorbar()

#-----------------------------------------------------------------------------#
# plot sample plane

sample_plane = pickle.load(open("sample_plane_intensity.pkl", 'rb'))

x = np.linspace(-64*0.1575, 64*0.1575, 129)
y = np.linspace(-64*0.1575, 64*0.1575, 129)

plt.figure(figsize = (6, 5))
plt.pcolor(x, y, sample_plane, cmap = 'jet') 
plt.colorbar()

