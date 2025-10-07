#!/bin/bash

# NREL HPC Job Script
# Generated on: 2025-10-06 17:36:29
# Job: saved_job

#SBATCH --account=csc000
#SBATCH --time=01:00:00
#SBATCH --job-name=saved_job
#SBATCH --nodes=1
#SBATCH --output=slurm-%j.out

# Job information
echo "Job started at: $(date)"
echo "Job ID: $SLURM_JOB_ID"
echo "Node(s): $SLURM_JOB_NODELIST"
echo "Number of nodes: $SLURM_JOB_NUM_NODES"
echo "Working directory: $PWD"
echo ""

# Job execution
# Add your job commands here
echo "Replace this with your actual job commands"

echo "Job completed at: $(date)"