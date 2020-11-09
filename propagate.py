#-----------------------------------------------------------------------------#
# Copyright (c) 2020 Institute of High Energy Physics Chinese Academy of 
#                    Science
#-----------------------------------------------------------------------------#

__authors__  = "Han Xu - HEPS Hard X-ray Scattering Beamline (B4)"
__date__     = "Date : 10.07.2020"
__version__  = "Alpha-2.0"


"""
propagate: The phase of lens; Kirchhoff-Fresnel integral. (multi process)

Functions: lens.
           source_spread.
           kirchhoff_integral.
           
Classes  : none.
"""

#-----------------------------------------------------------------------------#
# libraries

import numpy as np
import time
import _propagate
import mpi4py.MPI as mpi

from mpi4py.MPI import COMM_WORLD as multi_process

#-----------------------------------------------------------------------------#
# constants

# The number of the multi_process
process_number = mpi.COMM_WORLD.Get_size()

#-----------------------------------------------------------------------------#
# functions

def lens(front, mirror, mode):
    

    rank = multi_process.Get_rank()

    if rank == 0:
        result = _propagate._lens(front, mirror, mode)
    else:
        result = None

    recv_data = multi_process.bcast(result, root = 0)
    mirror.lens = recv_data

def source_spread(source, back):
    
    rank = multi_process.Get_rank()

    if rank == 0:
        result = _propagate._source_spread(source, back)
    else:
        result = None    
        
    # Broadcast
    recv_data = multi_process.bcast(result, root = 0)
    back.wavefront = recv_data[0]
    back.intensity = recv_data[1]

def kirchhoff_integral(front, back):
    
    rank = multi_process.Get_rank()
        
    source_count = front.source.source_count
    num = process_number
    
    p0 = source_count % (num - 1)
    p1 = source_count // (num - 1)
    parameters = list()
    
    if p0 == 0:
        
        for i in range(num - 1):
            
            parameters.append(range(p1*i, p1*(i + 1)))
            
    else:
        
        for i in range(num - 1):
            
            if i + 1 != num - 1:
                parameters.append(range(p1*i, p1*(i + 1)))
            else:
                parameters.append(range(p1*(num - 2), p1*(num - 1) + p0))
    
    if rank == 0:
        
        for i in range(num - 1):
            
            multi_process.Send([np.array(i), mpi.INT], 
                               dest = i + 1, tag = i + 1)
            
        for i in range(num - 1):
            
            isize = len(parameters[i])
            wavefronts = np.zeros(
                (isize, int(2*back.size[1] + 1), int(2*back.size[0] + 1)),
                dtype = np.complex128
                )

            multi_process.Recv(
                [wavefronts, mpi.COMPLEX], source = i + 1, tag = 100*i + 1
                )
        
            for k in range(isize):
                back.wavefront.append(wavefronts[k, :, :])
                
        back.intensity = np.sum(np.abs(np.array(back.wavefront))**2, 0)
    
    else:
        
        index = np.array(int())
        multi_process.Recv([index, mpi.INT], source = 0, tag = rank)
        
        results = [_propagate._point(i, front, back) 
                   for i in parameters[index]]

        multi_process.Send(
            [np.array(results), mpi.COMPLEX], 
            dest = 0, tag = 100*index + 1
            )
            