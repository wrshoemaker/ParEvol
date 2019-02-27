#!/bin/sh
#PBS -k o
#PBS -l nodes=1:ppn=8,vmem=100gb,walltime=24:00:00
#PBS -M wrshoema@iu.edu
#PBS -m abe
#PBS -m n
#PBS -j oe

# the location of the conda environment
# ~/.conda/envs/ParEvol/bin/python

module unload python/2.7.13
module load anaconda/python3.6/4.3.1
source activate ParEvol

# create asa159 Pyhon file to import
# f2py -c -m asa159 asa159.f90

# call that code from this file
python /N/dc2/projects/Lennon_Sequences/ParEvol/Python/run_analyses.py -f 1 -a -c
