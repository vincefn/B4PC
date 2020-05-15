# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 21:05:59 2020

@author: Han Xu
"""


################################################################################
# LIBARY

import numpy as np


###############################################################################
# FUNCTION

def _enveloped_phase(phase):

    return np.arctan2(np.cos(phase), -1*np.sin(phase))


def _lens(front, mirror, mode):
    
    """
    # Args:
    #     front：A class contains the properites of plane front.
    #     mirror: A class contains the properties of the mirror lens
    #     mode: if mode=1, long distance mode, the light of front plane is
                           treated as a point source
    #           if mode=0, the light of front plane is treated as a plane source

    # Return:
    #     A 2-dimensional arrays of complex wave front at back plane
    """
    
    if mode:
        
        lens_result = None
        
        # The divergent spherical wave at the crl incident phase
        dswave = (
            2*np.pi *
            np.sqrt((mirror.mesh[0]*mirror.pixel[0])**2 + (mirror.mesh[1]*mirror.pixel[1])**2 +
                    (mirror.location - front.location)**2
                    ) / mirror.source.wave_length
            )
        # The convergent spherical wave at the crl incident phase
        cswave = (
            2*np.pi *
            np.sqrt((mirror.mesh[0]*mirror.pixel[0])**2 + (mirror.mesh[1]*mirror.pixel[1])**2 +
                    (mirror.focus)**2
                    ) / mirror.source.wave_length
            )
        # The enveloped phase of mirror
        phase_lens = _enveloped_phase(-1*cswave + -1*dswave)
        lens_result = [phase_lens for i in range(mirror.source.source_count)]

    else:
        
        lens_result = []
        
        front_plane = [front.mesh[0].flatten(), front.mesh[1].flatten()]

        # iter the plane front for the optical path length
        for i in range(mirror.source.source_count):
            # The divergent spherical wave at the crl incident phase
            dswave = (
                2*np.pi *
                np.sqrt((mirror.mesh[0]*mirror.pixel[0] - front_plane[0][i]*front.pixel[0])**2 +
                        (mirror.mesh[1]*mirror.pixel[1] - front_plane[1][i]*front.pixel[1])**2 +
                        (mirror.location - front.location)**2
                        ) / mirror.source.wave_length
                )
            # The convergent spherical wave at the crl incident phase
            cswave = (
                2*np.pi *
                np.sqrt((mirror.mesh[0]*mirror.pixel[0] - front_plane[0][i]*front.pixel[0])**2 +
                        (mirror.mesh[1]*mirror.pixel[1] - front_plane[1][i]*front.pixel[1])**2 +
                        (mirror.focus)**2
                        ) / mirror.source.wave_length
                )
            phase_lens = _enveloped_phase(-1*cswave + -1*dswave)
            lens_result.append(phase_lens)
            
    return lens_result

def _source_spread(source, back):

    """
    # Args:
    #     source：A class contains the properites of source.
    #     back: A class contains the properties of plane back
    
    # Return:
    #     A 2-dimensional arrays of complex wave front at back plane
    """   
    
    # The propagation from source to the first element
    # if source.order == 0 and back.order == 1:
        
    # Initalize the wavefront of element back
    wavefront = np.array(np.copy(back.zero), dtype=complex)
    source_meshgrid = (source.mesh[0].flatten(), source.mesh[1].flatten())
    
    back_wavefront = []
    back_intensity = np.array(np.copy(back.zero))
    
    # the iteration of the source
    for i in range(source.source_count):
        # Calculate the wavefront under the effect of lens and error
        abs_wave = np.abs(source.wavefront[i])
        angle_wave = np.angle(source.wavefront[i])
        # Calcualte the optical length between source to first element
        source_back_length = np.sqrt(
            # The horizonal direction
            (source_meshgrid[0][i]*source.pixel[0] - back.mesh[0]*back.pixel[0])**2 +
            # The vertical direction
            (source_meshgrid[1][i]*source.pixel[1] - back.mesh[1]*back.pixel[1])**2 +
            # The z direction
            (back.location - source.location)**2
            )
        # The optical path fron source to back
        source_back_path = 2*np.pi * source_back_length / source.wave_length
#        wavefront = (
#            (abs_wave/source_back_length) *
#             np.exp(1j*(angle_wave + source_back_path))
#            )
        wavefront = abs_wave * np.exp(1j*(angle_wave + source_back_path))
        back_wavefront.append(wavefront)
        back_intensity = back_intensity + np.abs(wavefront)**2
    
    return [back_wavefront, back_intensity]

def _point(i, front, back):

    # Initalize the wavefront of element back
    wavefront = np.array(np.copy(back.zero.flatten()), dtype=complex)
    back_meshgrid = (back.mesh[0].flatten(), back.mesh[1].flatten())
    
    # Calculate the wavefront under the effect of lens and error
    abs_wave = np.abs(front.wavefront[i])
    angle_wave = np.angle(front.wavefront[i]) + front.lens[i] + front.error 
    
    # The iteration of the front plane
    for k in range(back.count):

        # The optical length between front to back
        front_back_length = np.sqrt(
            # The horizonal direction
            (back_meshgrid[0][k]*back.pixel[0] - front.mesh[0]*front.pixel[0])**2 +
            # The vertical direction
            (back_meshgrid[1][k]*back.pixel[1] - front.mesh[1]*front.pixel[1])**2 +
            # The z direction
            (back.location - front.location)**2
            )
        # The optical path fron front to back
        front_back_path = 2*np.pi * front_back_length / front.source.wave_length
        # The angle factor in Kirchhoff integral
        costhe = np.abs(back.location - front.location) / front_back_length
        # The integral process
        wavefront[k] = wavefront[k] + np.sum(
            # The integral area
            front.pixel[0]*front.pixel[1] *
            abs_wave *
            np.exp(1j*(angle_wave + front_back_path)) *
            costhe / 
            (front.source.wave_length*front_back_length)
            )
 
    # The wavefront of point source
    wavefront = np.reshape(wavefront, (2*back.size[1] + 1, 2*back.size[0] + 1))
    return wavefront
        
def _kirchhoff_integral(front, back):

    """
    # Args:
    #     front：A class contains the properites of plane front.
    #     back: A dict contains the properties of plane back

    # Return:
    #     A 2-dimensional arrays of complex wave front at back plane

    # The meshed plane of front
    """
    
    back_wavefront = [_point(i, front, back) for i in range(front.source.source_count)]
    back_intensity = np.sum(np.abs(np.array(back_wavefront))**2, 0)
    back.wavefront = back_wavefront
    back.intensity = back_intensity
        
