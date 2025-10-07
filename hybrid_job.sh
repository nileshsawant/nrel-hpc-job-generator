#!/bin/bash

# NREL HPC Job Script
# Generated on: 2025-10-06 17:37:17
# Job: hybrid-mpi-openmp

#SBATCH --account=csc000
#SBATCH --time=04:00:00
#SBATCH --job-name=hybrid-mpi-openmp
#SBATCH --partition=standard
#SBATCH --nodes=4
#SBATCH --ntasks=16
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=8
#SBATCH --mem=200GB
#SBATCH --output=slurm-%j.out

# Job information
echo "Job started at: $(date)"
echo "Job ID: $SLURM_JOB_ID"
echo "Node(s): $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Working directory: $PWD"
echo ""

# Load required modules
module load python/3.9
module load openmpi
module load mkl

# Job execution
# MPI/Parallel execution with srun
export OMP_NUM_THREADS=8
srun --ntasks=16 --ntasks-per-node=4 --cpus-per-task=8 python large_scale_simulation.py

echo "Job completed at: $(date)"