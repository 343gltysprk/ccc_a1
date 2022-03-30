#!/bin/bash
#SBATCH	--ntasks=1
module load foss/2019b
module load python/3.7.4
module --ignore-cache load mpi4py/3.0.2-timed-pingpong
srun -n 1 python3 parallel.py sydGrid.json bigTwitter.json 

my-job-stats -a -n -s

