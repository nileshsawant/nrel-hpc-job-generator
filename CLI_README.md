# NREL HPC Job Script Generator - CLI Tool

A command-line interface for generating NREL Kestrel HPC Slurm job scripts directly on the HPC system.

## Quick Start

### Installation on Kestrel

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nileshsawant/nrel-hpc-job-generator.git
   cd nrel-hpc-job-generator
   ```

2. **Run the installer (optional):**
   ```bash
   ./install.sh
   ```
   This installs the tool to `~/bin/` and creates a `nrel-jobgen` command.

3. **Or use directly:**
   ```bash
   python3 generate_job.py --help
   ```

## Usage Examples

### Interactive Mode (Recommended for Beginners)
```bash
python3 generate_job.py --interactive
```

### Command Line Examples

**Basic job:**
```bash
python3 generate_job.py --account csc000 --time 01:00:00 --job-name my_job
```

**Multi-node job with specific resources:**
```bash
python3 generate_job.py \
  --account csc000 \
  --time 2:00:00 \
  --job-name parallel_job \
  --nodes 4 \
  --ntasks 128 \
  --ntasks-per-node 32 \
  --partition standard
```

**GPU job:**
```bash
python3 generate_job.py \
  --account csc000 \
  --time 30 \
  --partition debug \
  --gpus 1 \
  --job-name gpu_test \
  --modules cuda/11.8 \
  --commands "nvidia-smi" "python my_gpu_script.py"
```

**Save to file and submit:**
```bash
python3 generate_job.py \
  --account csc000 \
  --time 01:00:00 \
  --job-name production_run \
  --nodes 2 \
  --ntasks 64 \
  --memory 100GB \
  --mail-user your.email@nrel.gov \
  --modules "python/3.9" "gcc/8.4.0" \
  --commands "python analysis.py" \
  --save job_script.sh \
  --submit
```

**Using a script file for commands:**
```bash
# Create a file with your commands
echo "python preprocess.py" > commands.txt
echo "python main_analysis.py" >> commands.txt
echo "python postprocess.py" >> commands.txt

python3 generate_job.py \
  --account csc000 \
  --time 4:00:00 \
  --job-name workflow \
  --script-file commands.txt \
  --save workflow.sh
```

## Command Reference

### Required Parameters
- `--account, -A`: Your NREL project account (e.g., `csc000`)
- `--time, -t`: Walltime in format `HH:MM:SS`, `D-HH:MM:SS`, or minutes

### Job Configuration
- `--job-name, -J`: Name for your job
- `--partition, -p`: Partition (debug, short, standard, long)
- `--qos`: Quality of service (normal, high, standby)

### Resources
- `--nodes, -N`: Number of compute nodes (default: 1)
- `--ntasks, -n`: Total number of MPI tasks
- `--ntasks-per-node`: Tasks per node
- `--cpus-per-task, -c`: CPUs per task (for threading)
- `--memory, --mem`: Memory per node (e.g., `50GB`)
- `--memory-per-cpu`: Memory per CPU (e.g., `2GB`)
- `--gpus, -G`: Number of GPUs
- `--tmp`: Local scratch space (e.g., `100GB`)

### Notifications
- `--mail-user`: Email for job notifications
- `--mail-type`: When to email (default: `END,FAIL`)

### Job Content
- `--modules`: Space-separated list of modules to load
- `--commands`: Space-separated list of commands to run
- `--script-file`: File containing commands to execute

### Output Options
- `--save, -s`: Save script to specified file
- `--submit`: Automatically submit the job (requires `--save`)

## NREL Kestrel Specific Information

### Partitions and Time Limits
- **debug**: 30 minutes max, for testing
- **short**: 4 hours max, higher priority
- **standard**: 24 hours max, normal queue
- **long**: 48 hours max, for long runs

### Typical Node Configurations
- **Standard compute**: 104 cores, ~250GB RAM per node
- **GPU nodes**: Various GPU types available
- **High memory**: Up to 1TB RAM on special nodes

### Account Format
Your account handle typically starts with your organization code:
- `csc###` for CSC projects
- `bioE###` for EERE Bioenergy projects  
- `h2###` for H2@Scale projects
- etc.

## Tips for Kestrel Users

### 1. Check Your Account
```bash
sacctmgr show user $USER -s
```

### 2. Monitor Job Progress
```bash
squeue -u $USER
```

### 3. Check Job Details
```bash
scontrol show job <job_id>
```

### 4. Cancel a Job
```bash
scancel <job_id>
```

### 5. View Job History
```bash
sacct -u $USER
```

## Advanced Examples

### Array Job
```bash
python3 generate_job.py \
  --account csc000 \
  --time 01:00:00 \
  --job-name array_job \
  --commands "python process_file_\$SLURM_ARRAY_TASK_ID.py" \
  --save array_job.sh

# Manually add array directive to the generated script
echo "#SBATCH --array=1-10" >> array_job.sh
```

### Dependency Chain
```bash
# Generate first job
python3 generate_job.py \
  --account csc000 \
  --time 01:00:00 \
  --job-name preprocess \
  --commands "python preprocess.py" \
  --save preprocess.sh

# Submit and capture job ID
JOB1=$(sbatch preprocess.sh | awk '{print $4}')

# Generate dependent job
python3 generate_job.py \
  --account csc000 \
  --time 02:00:00 \
  --job-name analysis \
  --commands "python analysis.py" \
  --save analysis.sh

# Submit with dependency (manual)
sbatch --dependency=afterok:$JOB1 analysis.sh
```

## Troubleshooting

### Common Issues

1. **"Invalid account"**: Check your account with `sacctmgr show user $USER -s`
2. **"Invalid partition"**: Use `sinfo` to see available partitions
3. **"Job pending"**: Check queue status with `squeue` or `sinfo`
4. **"Out of memory"**: Increase memory request or reduce resource usage

### Getting Help

1. **Check Kestrel documentation**: https://nrel.gov/hpc/kestrel/
2. **Contact HPC support**: hpc-help@nrel.gov
3. **View system status**: `sinfo -s`

## Integration with Other Tools

### With VS Code (Remote SSH)
```bash
# Generate script on Kestrel via VS Code terminal
python3 generate_job.py --interactive
```

### With Jupyter
```bash
# Generate job to run Jupyter notebook
python3 generate_job.py \
  --account csc000 \
  --time 01:00:00 \
  --job-name jupyter_job \
  --modules "python/3.9" \
  --commands "jupyter nbconvert --execute my_notebook.ipynb" \
  --save jupyter_job.sh
```

### Batch Generation
```bash
# Create multiple similar jobs
for i in {1..5}; do
  python3 generate_job.py \
    --account csc000 \
    --time 01:00:00 \
    --job-name "job_$i" \
    --commands "python process_part_$i.py" \
    --save "job_$i.sh"
done
```

---

**Note**: This CLI tool generates standard Slurm scripts for NREL Kestrel. Always verify generated scripts match your job requirements before submission.