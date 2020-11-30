#-----------------------------------------------------------------------------#
# Copyright (c) 2020 Institute of High Energy Physics Chinese Academy of 
#                    Science
#-----------------------------------------------------------------------------#

__authors__  = "Han Xu - HEPS Hard X-ray Scattering Beamline (B4)"
__date__     = "Date : 10.07.2020"
__version__  = "Alpha-2.0"


"""
propagate: The phase of lens; Kirchhoff-Fresnel integral. (multi process)

Functions: none.
           
Classes  : LightSource.
           OpticElements.
           TestCoherentMdoes.
           
"""

#-----------------------------------------------------------------------------#
# libraries

import numpy as np
import pickle
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------#
# functions


#-----------------------------------------------------------------------------#
# classes


class LightSource(object):
    """Given the parameters, a weighted point source model will be generated."""

    def __init__(
            self,
            name="source",
            order=0,
            source_count=None,
            wave_length=None,
            source_sigma=[None, None],
            optic_location=0,
            optic_planesize=[None, None],
            optic_pixelsize=[None, None],
            ):
        
        """Return the properites of an optical elments.

        # Args:
        #     source: The source parameters, includes
        #             [pixel number of source,
        #              wave_length of source,
        #              gaussian sigma of source].
        #     plane: The opitcal plane parameters, includes
        #            [location of the optical plane,
        #             mesh size of the plane,
        #             pixel length of mesh,
        #             the pixel number of optical plane].
        #     foci: The focal length of the lens (crl....).

        # Return:
        """
        # The name of the element
        self.name = name
        
        # The order of this element in the optical layout
        self.order = order
        self.source_count = source_count
        self.wave_length = wave_length
        self.sigma = source_sigma
        
        # The structure of the plane
        self.location = optic_location
        self.size = optic_planesize
        self.pixel = optic_pixelsize

        if isinstance(self.size[0], int):
            # The zero matrix of an optical plane
            self.zero = np.zeros([2*self.size[1] + 1, 2*self.size[0] + 1])
            # The meshgrid of an optical plane
            self.mesh = np.meshgrid(
                np.linspace(-1*self.size[0], self.size[0], 2*self.size[0] + 1),
                np.linspace(-1*self.size[1], self.size[1], 2*self.size[1] + 1)
                )
        elif self.size is None:
            self.zero = None
            self.mesh = None

        # The wavefront of this plane
        self.wavefront = None
        self.intensity = np.copy(self.zero)
        self.amplitude = np.copy(self.zero)
        self.phase = np.copy(self.zero)

    def gauss_source(self):
        """Given the gaussian paramters, generate a gauss source.

        # The phase is generated randomly. The intensity is gaussian,
        # the amplitude is not.

        # Args:
        #    pixel_size: The actual size of a pixel of plane [hor, ver].
        #                unit: um.
        #    plane: The meshgrid plane of the source.
        #     sigma: The parameters sigma of gaussian.

        # Return:
        #     The intensity, amplitude, phase and the wavefront of source.
        """
        self.intensity = (np.exp(-1*self.pixel[0] *
                                 (self.pixel[0] * np.abs(self.mesh[0]))**2 /
                                 self.sigma[0]**2
                                 ) *
                          np.exp(-1*self.pixel[1] *
                                 (self.pixel[1] * np.abs(self.mesh[1]))**2 /
                                 self.sigma[1]**2
                                 ) /
                          (2*np.pi * self.sigma[0]*self.sigma[1])
                          )

        self.amplitude = np.sqrt(self.intensity)
        self.phase = 2*np.pi * np.random.rand(np.shape(self.mesh[0])[0],
                                              np.shape(self.mesh[0])[1])
        self.wavefront = self.amplitude*np.exp(1j*self.phase)
        self.wavefront = self.wavefront.flatten()
        
    def show(self):
        """Plot the intensity of the plane.
        """
        plt.imshow(self.intensity)
        
    def save(self):
        """Save the element.
        """
        with open(self.name + ".pkl", "wb") as file:
            pickle.dump(self, file)
            file.close()
        np.savez_compressed(self.name + ".npz", intensity=self.intensity,amplitude=self.amplitude, phase=self.phase)
            
            
class OpticElements(object):
    """Given the parameters, the class of opical plane will be generated."""

    def __init__(
            self,
            source_class=None,
            name=None,
            order=None,
            optic_location=None,
            optic_planesize=[None, None],
            optic_pixelsize=[None, None],
            optic_planecount=None,
            optic_focus=None,
            ):
        """Return the properites of an optical elments.

        # Args:
        #     source: An instance of class Source.
        #     plane: The opitcal plane parameters, includes
        #            [location of the optical plane,
        #             mesh size of the plane,
        #             pixel length of mesh,
        #             the pixel number of optical plane].
        #     foci: The focal length of the lens (crl....).

        # Return:
        """
        # The name of the element
        self.name = name
        # The order of this element in the optical layout
        self.order = order
        # The optic source of this optic system
        self.source = source_class
        # The parameters of len
        self.focus = optic_focus
        # The structure of the plane
        self.location = optic_location
        self.size = optic_planesize
        self.pixel = optic_pixelsize
        self.count = optic_planecount

        if isinstance(self.size[0], int):
            # The zero matrix of an optical plane
            self.zero = np.zeros([2*self.size[1] + 1, 2*self.size[0] + 1])
            # The meshgrid of an optical plane
            self.mesh = np.meshgrid(
                np.linspace(-1*self.size[0], self.size[0], 2*self.size[0] + 1),
                np.linspace(-1*self.size[1], self.size[1], 2*self.size[1] + 1)
                )
        elif self.size is None:
            self.zero = None
            self.mesh = None

        # The phase error of plane
        self.error = np.copy(self.zero)
        # The wavefront of this plane
        self.wavefront = []
        self.intensity = np.copy(self.zero)
        self.amplitude = np.copy(self.zero)
        self.phase = np.copy(self.zero)
        # The phase changed induced by lens
        self.lens = [np.copy(self.zero) for i in range(source_class.source_count)]
        self.mask = None
        
    def save(self):
        """Save the element.
        """
        with open(self.name + ".pkl", "wb") as file:
            pickle.dump(self, file)
            file.close()
        np.savez_compressed(self.name + ".npz", intensity=self.intensity, amplitude=self.amplitude, phase=self.phase, wavefront=np.array(self.wavefront), lens=np.array(self.lens))
    
    def save_without_wavefronts(self):
        """Save the element without the wavefronts"""
        self.wavefront = list()
        with open(self.name + "_nowfrs.pkl", "wb") as file:
            pickle.dump(self, file)
            file.close()
        
    def show(self):
        """Plot the intensity of the plane.
        """
        plt.imshow(self.intensity)


class TestCoherentMode(object):
    """Test the coherent mode propagation."""
    
    def __init__(
            self,
            element_class = None,
            n = 25
            ):
        
        self.mode = []
        self.eig_value = []
        self.n = n
        self.J = None
        self.element = element_class
    
    def create_mode(self):
        
        from mathmatrix import arnoldi
        
        wavefront = np.array(self.element.wavefront)
        repeats, sx, sy = wavefront.shape
        wavefront = np.reshape(wavefront, (repeats, sx*sy))
        
        self.J = np.dot(wavefront.T.conjugate(), wavefront)
        self.eig_value, eig_vector = arnoldi(self.J, num_eigvectors = self.n)
        self.mode = [np.reshape(np.matrix(eig_vector[i, :]), (sx, sy)) for i in range(self.n)]
        
        
    def create_J(self):
        
        mode = np.array(self.mode)
        num, sx, sy = mode.shape
        mode = np.reshape(mode, (num, sx*sy))
        
        for i in range(num):
            mode[i, :] = mode[i, :]*self.eig_value[i]
        mode = np.matrix(mode)
        self.J = np.dot(mode.T.conjugate(), mode)
        
    