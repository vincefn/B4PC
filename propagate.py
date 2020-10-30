# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 16:16:45 2020

@author: Han Xu
"""


###############################################################################
# LIBARY

import numpy as np
import time
import _propagate
from mpi4py.MPI import COMM_WORLD as multi_process


###############################################################################
# CONSTANT

# The number of the multi_process
process_number = 10


###############################################################################
# FUNCTION

def lens(front, mirror, mode):
    
    # Get the current process
    rank = multi_process.Get_rank()
    # The generation of phase of lens is not time-costing and only process 0 is used
    if rank == 0:
        result = _propagate._lens(front, mirror, mode)
    else:
        result = None
    # Broadcast the result to all the process for the following calculation
    recv_data = multi_process.bcast(result, root = 0)
    mirror.lens = recv_data

def source_spread(source, back):
    
    # Get the current process
    rank = multi_process.Get_rank()
    # not time-costing
    if rank == 0:
        result = _propagate._source_spread(source, back)
    else:
        result = None    
        
    # Broadcast
    recv_data = multi_process.bcast(result, root = 0)
    back.wavefront = recv_data[0]
    back.intensity = recv_data[1]

def kirch_integral(front, back):

    print(time.ctime())
    
    rank = multi_process.Get_rank()
    
    print(rank)
    
    result = []
    back_wavefront = []
    back_intensity = None
    
    source_count = back.source.source_count
    num = process_number
    p = source_count % (num - 1)
    cell = int((source_count - p) / (num - 1))
    
    if rank == 0:
        # this k is used to define the order
        parameters = [[range((k - 1)*cell, k*cell), k]  for k in range(1, num)]
        parameters.append([range(source_count - p, source_count), num])
    else:
        parameters = None
    
    # scattering the paramters from process root (rank == 0)
    recv_count = multi_process.scatter(parameters, root = 0)
    # recvie the parameters
    parameter_part = recv_count
    # calculate the wavefront of one point source
    result.append(parameter_part[1])
    result.append([_propagate._point(i, front, back) for i in parameter_part[0]])
    # recive the data
    recv_data = multi_process.gather(result, root = 0)
    # organize the reuslt
    if rank == 0:
        for part in recv_data:
            for i in range(1, num + 1):
                if part[0] == i:
                    for single_wavefront in part[1]:
                        back_wavefront.append(single_wavefront)
    
    if len(back.wavefront) == source_count:
        back_intensity = np.sum(np.abs(np.array(back.wavefront))**2, 0)

#    back_result = multi_process.bcast([back_wavefront, back_intensity], root = 0)
#    back.wavefront = back_result[0]
#    back.intensity = back_result[1]    
    
    back.wavefront = back_wavefront
    back.intensity = np.sum(np.abs(np.array(back.wavefront))**2, 0)

    print(time.ctime())
    
        
