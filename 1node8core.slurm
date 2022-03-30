#!/bin/bash
#SBATCH	--nodes=1 --ntasks=8
module load foss/2019b
module load python/3.7.4
module --ignore-cache load mpi4py/3.0.2-timed-pingpong
srun -n 8 python3 parallel.py sydGrid.json bigTwitter.json 

my-job-stats -a -n -s

