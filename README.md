## B4PC

"A Wave Optics Model for the Effect of Partial Coherence on Coherent Diffractive Imaging"

alpha version 

python version: 3.7
python environment: anaconda
packages：
* numpy      1.18.4
* mpi4py     3.0.3
* matplotlib 3.2.1
          

## Examples

Two examples are provided:

1. The simulation of secondary source (Figure.2 of paper);
2. The simulation of the intensity at the sample palne (Figure.7a of the paper).

Both examples have been verifed in a desktop.
* CPU：Intel(R) Core(TM) i7-6700 CPU @ 3.40GHZ 3.41GHZ
* RAM: 16.0GB

## Operation

Example 1: mpiexec -n k python secondary_source.py

Example 2: mpiexec -n k python slit.py; 
           mpiexec -n k python sample_plane.py

For the computer for verification, k was set as 6.

A successful calculation will generates three files:
* secondary_source.pkl;
* slit.pkl;
* sample_plane.pkl.

The secondary_source.pkl and sample_plane.pkl can be shown by plot.py.

If you have any other questions please feel free to contact me:
xuhan@ihep.ac.cn

