# NREL HPC Job Script Generator

A web-based application for generating Slurm batch scripts for NREL High Performance Computing systems, specifically designed for the Kestrel supercomputer.

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

### For Users (No Installation Required)

**Option 1: GitHub Codespaces** (Recommended for NREL researchers)
1. Visit the [GitHub repository](https://github.com/nileshsawant/nrel-hpc-job-generator)
2. Click "Code" → "Create codespace on main"
3. Wait for the environment to load
4. In the terminal, run: `./start.sh`
5. Click "Open in Browser" when prompted, or use the PORTS tab
6. Use the web interface to generate job scripts!

**Option 2: Live Web App**
- Visit: `https://your-app-name.railway.app` (or Heroku/Render URL)
- Start generating job scripts immediately!

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
   ```
   http://localhost:5000
   ```

### 📋 Ready to Deploy?
See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for complete deployment instructions to various platforms.

### Usage

1. **Fill out the form**: Enter your job requirements using the web interface
2. **Review the script**: Generated script appears in real-time on the right panel
3. **Download**: Click "Download Script" to save the `.sh` file
4. **Submit**: Upload the script to your HPC system and submit with `sbatch`

## Generated Script Features

The generated scripts include:

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

## Configuration Options

### Required Parameters
- **Account**: Your NREL HPC project allocation
- **Walltime**: Maximum job duration

### Resource Requests
- **Nodes**: Number of compute nodes
- **Tasks**: Total number of MPI tasks
- **CPUs per Task**: Threading configuration
- **Memory**: RAM requirements (per node or per CPU)
- **GPUs**: GPU resource allocation
- **Local Storage**: Scratch space requirements

### Job Management
- **Partition**: Queue selection (debug, standard, long)
- **QOS**: Priority level (normal, high, standby)
- **Email Notifications**: Job status updates
- **Output Files**: Stdout/stderr redirection

### Environment Setup
- **Modules**: Software environment loading
- **Environment Variables**: Custom configuration
- **Job Commands**: Your application execution

## Best Practices

The generator incorporates NREL HPC best practices:

- **Resource Efficiency**: Guidance on right-sizing requests
- **File System Usage**: Proper paths for executables and data
- **Queue Selection**: Appropriate partition for job duration
- **Error Handling**: Robust job completion logging
- **Documentation**: Clear script comments and headers

## File Structure

```
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # HTML template base
│   ├── index.html        # Main generator interface
│   └── examples.html     # Example scripts page
└── README.md             # This file
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