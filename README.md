# NREL HPC Job Script Generator

A comprehensive solution for generating Slurm batch scripts for NREL High Performance Computing systems, specifically designed for the Kestrel supercomputer.

## 🎯 Multiple Access Methods

- **🌐 Web Interface**: User-friendly browser-based generator
- **💻 Command Line Interface**: Direct CLI tool for use on Kestrel
- **📱 Standalone HTML**: Offline-capable single-file version

## Features

- **Interactive Web Interface**: Easy-to-use form for configuring job parameters
- **Real-time Validation**: Input validation with helpful error messages
- **Live Preview**: See generated script as you type
- **Download Scripts**: Save generated scripts as `.sh` files
- **Example Library**: Common job script patterns and templates
- **NREL-Specific**: Tailored for NREL HPC systems and best practices

## Supported Job Types

- CPU jobs (debug, standard, long partitions)
- GPU jobs with resource allocation
- MPI jobs with multi-node configurations  
- Memory-intensive jobs
- Jobs with local scratch storage requirements

## 🚀 Quick Start

### For Developers (Local Development)

#### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

#### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/nileshsawant/nrel-hpc-job-generator.git
   cd nrel-hpc-job-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to:
   ```bash
   http://localhost:5000
   ```

### 📋 Ready to Deploy?
See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for complete deployment instructions to various platforms.

## 🖥️ Command Line Interface (CLI)

For users working directly on Kestrel, we provide a powerful CLI tool that generates the same high-quality job scripts with full command-line control.

### CLI Installation on Kestrel

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

### CLI Usage Examples

#### Interactive Mode (Recommended for Beginners)
```bash
python3 generate_job.py --interactive
```

#### Command Line Examples

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

### CLI Command Reference

#### Required Parameters
- `--account, -A`: Your NREL project account (e.g., `csc000`)
- `--time, -t`: Walltime in format `HH:MM:SS`, `D-HH:MM:SS`, or minutes

#### Job Configuration
- `--job-name, -J`: Name for your job
- `--partition, -p`: Partition (debug, short, standard, long)
- `--qos`: Quality of service (normal, high, standby)

#### Resources
- `--nodes, -N`: Number of compute nodes (default: 1)
- `--ntasks, -n`: Total number of MPI tasks
- `--ntasks-per-node`: Tasks per node
- `--cpus-per-task, -c`: CPUs per task (for threading)
- `--memory, --mem`: Memory per node (e.g., `50GB`)
- `--memory-per-cpu`: Memory per CPU (e.g., `2GB`)
- `--gpus, -G`: Number of GPUs
- `--tmp`: Local scratch space (e.g., `100GB`)

#### Output Options
- `--save, -s`: Save script to specified file
- `--submit`: Automatically submit the job (requires `--save`)

### NREL Kestrel Specific Information

#### Partitions and Time Limits
- **debug**: 1 hour max, for testing (1 job per user, max 2 nodes)
- **short**: 4 hours max, for shorter jobs (2240 nodes total)
- **standard**: 2 days max, normal queue (2240 nodes, 1050 per user)
- **long**: 10 days max, for long runs (430 nodes, 215 per user)
- **shared**: 2 days max, shared nodes (128 nodes, half partition per user)
- **sharedl**: 10 days max, shared nodes for long jobs (32 nodes, 16 per user)
- **hbw**: 2 days max, high bandwidth nodes with dual NICs (min 2 nodes, 512 total)
- **hbwl**: 10 days max, high bandwidth nodes for long jobs (128 nodes, 64 per user)
- **medmem**: 10 days max, medium memory nodes with 1TB RAM (64 nodes, 32 per user)
- **bigmem**: 2 days max, big memory nodes with 2TB RAM (10 nodes, 4 per user)
- **bigmeml**: 10 days max, big memory nodes for long jobs (4 nodes, 2 per user)
- **nvme**: 2 days max, nodes with 1.7TB NVMe local drives (256 nodes, 128 per user)
- **gpu-h100**: 2 days max, GPU nodes with 4 NVIDIA H100 GPUs (156 nodes total)
- **gpu-h100s**: 4 hours max, GPU nodes for short jobs (156 nodes total)
- **gpu-h100l**: 10 days max, GPU nodes for long jobs (39 nodes total)

#### Typical Node Configurations
- **Standard CPU nodes**: 104 cores, 240GB usable RAM per node
- **GPU nodes**: 4 NVIDIA H100 GPUs (80GB each), 128 cores, 350-1440GB RAM
- **Medium memory nodes**: 104 cores, 1TB RAM (64 nodes available)
- **Big memory nodes**: 104 cores, 2TB RAM, 5.6TB NVMe (10 nodes available)
- **High bandwidth nodes**: 104 cores, dual NICs, some with 1TB RAM (512 nodes)
- **NVMe nodes**: 104 cores, 1.7TB local NVMe storage (256 nodes)

#### Account Format
Your account handle typically starts with your organization code:
- `csc###` for CSC projects
- `bioE###` for EERE Bioenergy projects  
- `h2###` for H2@Scale projects
- etc.

### CLI Advanced Examples

#### Array Job
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

#### Batch Generation
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

### CLI Tips for Kestrel Users

1. **Check Your Account**: `sacctmgr show user $USER -s`
2. **Monitor Job Progress**: `squeue -u $USER`
3. **Check Job Details**: `scontrol show job <job_id>`
4. **Cancel a Job**: `scancel <job_id>`
5. **View Job History**: `sacct -u $USER`

## 🌐 Web Interface Options

### For NREL Users (Policy Compliant)

**Option 1: Standalone HTML File** ⭐ **RECOMMENDED**
1. Download `standalone.html` from this repository
2. Open the file in any web browser (Chrome, Firefox, Safari)
3. Generate job scripts entirely offline - no external servers needed!
4. **Benefits:** NREL policy compliant, works offline, no data transmission

**Option 2: Local Web Server**
1. Follow the "For Developers" installation steps above
2. Access at `http://localhost:5000` on your computer

**Option 3: GitHub Codespaces** (if network allows)
1. Visit the [GitHub repository](https://github.com/nileshsawant/nrel-hpc-job-generator)
2. Click "Code" → "Create codespace on main"  
3. Run: `./start-minimal.sh` (for better network reliability)
4. Use the PORTS tab to access the web interface

### Web Interface Usage

1. **Fill out the form**: Enter your job requirements using the web interface
2. **Review the script**: Generated script appears in real-time on the right panel
3. **Download**: Click "Download Script" to save the `.sh` file
4. **Submit**: Upload the script to your HPC system and submit with `sbatch`

## Generated Script Features

Both the CLI and web interface generate scripts with:

- **Proper SBATCH directives** for resource allocation
- **Job information logging** (job ID, nodes, timestamps)
- **Module loading** for software environments
- **Environment setup** commands
- **Error handling** and job completion notifications
- **NREL-specific** environment variables and paths

## Example Scripts

The application includes example scripts for:

- **CPU Debug Job**: Quick testing in debug partition
- **GPU Job**: Single or multi-GPU resource allocation
- **MPI Job**: Multi-node parallel computing setup

## Best Practices

The generator incorporates NREL HPC best practices:

- **Resource Efficiency**: Guidance on right-sizing requests
- **File System Usage**: Proper paths for executables and data
- **Queue Selection**: Appropriate partition for job duration
- **Error Handling**: Robust job completion logging
- **Documentation**: Clear script comments and headers

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

## File Structure

```
├── app.py                 # Flask web application
├── generate_job.py        # CLI tool
├── install.sh            # CLI installer
├── demo.sh              # CLI demonstration
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # HTML template base
│   ├── index.html        # Main generator interface
│   └── examples.html     # Example scripts page
├── standalone.html       # Offline HTML version
└── README.md            # This file
```

## Development

### Adding New Features

The application is built with Flask and uses Bootstrap for styling. Key components:

- `JobScriptGenerator` class: Core script generation logic
- Form validation: Client and server-side input checking
- Templates: Jinja2 templates with Bootstrap styling
- JavaScript: Real-time form interaction and AJAX requests

### Customization

To customize for other HPC systems:

1. Update `partitions` and `qos_options` in `JobScriptGenerator`
2. Modify script template in `generate_script()` method
3. Adjust validation rules in `validate_inputs()` method
4. Update examples and documentation

## Contributing

When contributing:

1. Test thoroughly with various job configurations
2. Validate generated scripts on actual HPC systems
3. Follow NREL HPC documentation guidelines
4. Update examples and documentation as needed

## Support

For issues related to:

- **This application**: Check the generated script syntax and validation
- **NREL HPC systems**: Consult [NREL HPC Documentation](https://nrel.github.io/HPC/)
- **Slurm scheduler**: Review [Slurm documentation](https://slurm.schedmd.com/)

## License

This project is provided as-is for NREL HPC users. Generated scripts should always be reviewed before submission to ensure they meet your specific requirements and follow current NREL HPC policies.

---

**Important**: Always verify generated scripts match your job requirements and current NREL HPC system configurations before submitting to the queue.