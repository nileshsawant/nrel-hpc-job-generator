from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime, timedelta
import re

app = Flask(__name__)

class JobScriptGenerator:
    """Generator for NREL HPC Slurm job scripts"""
    
    def __init__(self):
        self.partitions = {
            'debug': {'max_time': '01:00:00', 'description': 'Debug partition (1 hour max, 1 job per user, max 2 nodes)'},
            'short': {'max_time': '04:00:00', 'description': 'Jobs with walltimes <= 4 hours (2240 nodes total)'},
            'standard': {'max_time': '2-00:00:00', 'description': 'Jobs with walltimes <= 2 days (2240 nodes, 1050 per user)'},
            'long': {'max_time': '10-00:00:00', 'description': 'Jobs with walltimes > 2 days (430 nodes, 215 per user)'},
            'shared': {'max_time': '2-00:00:00', 'description': 'Shared nodes (128 nodes, half partition per user)'},
            'sharedl': {'max_time': '10-00:00:00', 'description': 'Shared nodes for long jobs (32 nodes, 16 per user)'},
            'hbw': {'max_time': '2-00:00:00', 'description': 'High bandwidth nodes with dual NICs (min 2 nodes, 512 total)'},
            'hbwl': {'max_time': '10-00:00:00', 'description': 'High bandwidth nodes for long jobs (128 nodes, 64 per user)'},
            'medmem': {'max_time': '10-00:00:00', 'description': 'Medium memory nodes with 1TB RAM (64 nodes, 32 per user)'},
            'bigmem': {'max_time': '2-00:00:00', 'description': 'Big memory nodes with 2TB RAM (10 nodes, 4 per user)'},
            'bigmeml': {'max_time': '10-00:00:00', 'description': 'Big memory nodes for long jobs (4 nodes, 2 per user)'},
            'nvme': {'max_time': '2-00:00:00', 'description': 'Nodes with 1.7TB NVMe local drives (256 nodes, 128 per user)'},
            'gpu-h100': {'max_time': '2-00:00:00', 'description': 'GPU nodes with 4 NVIDIA H100 GPUs (156 nodes total)'},
            'gpu-h100s': {'max_time': '04:00:00', 'description': 'GPU nodes for short jobs <= 4 hours (156 nodes total)'},
            'gpu-h100l': {'max_time': '10-00:00:00', 'description': 'GPU nodes for long jobs > 2 days (39 nodes total)'}
        }
        
        self.qos_options = {
            'normal': {'multiplier': 1.0, 'description': 'Normal priority'},
            'high': {'multiplier': 2.0, 'description': 'High priority (2x AU cost)'},
            'standby': {'multiplier': 0.0, 'description': 'Standby (free, runs when idle)'}
        }
        
        self.application_templates = {
            'general': {
                'name': 'General Template',
                'description': 'Standard job script template for general HPC workloads',
                'modules': [],
                'environment': [],
                'default_command': 'echo "Replace this with your command"',
                'mpi_flags': [],
                'recommended_partition': None,
                'partition_reason': None
            },
            'gaussian': {
                'name': 'Gaussian Template',
                'description': 'Optimized for Gaussian16 quantum chemistry calculations',
                'modules': ['gaussian'],
                'environment': [
                    'export GAUSS_SCRDIR=$TMPDIR',
                    'export GAUSS_MEMDEF=2GB'
                ],
                'default_command': 'g16_nrel < input.gjf > output.log',
                'mpi_flags': [],
                'recommended_partition': 'nvme',
                'partition_reason': 'I/O intensive calculations benefit from fast local storage'
            },
            'lammps': {
                'name': 'LAMMPS Template',
                'description': 'Configured for LAMMPS molecular dynamics simulations',
                'modules': ['lammps/080223-intel-mpich'],
                'environment': [],
                'default_command': 'lmp -in input.in',
                'mpi_flags': ['--mpi=pmi2'],
                'recommended_partition': 'hbw',
                'partition_reason': 'High-bandwidth partition recommended for >10 nodes'
            },
            'ansys': {
                'name': 'ANSYS Template',
                'description': 'Setup for ANSYS Fluent and Mechanical simulations',
                'modules': ['ansys'],
                'environment': [
                    'export FLUENT_AFFINITY=0',
                    'export SLURM_ENABLED=1',
                    'export SCHEDULER_TIGHT_COUPLING=13',
                    'export I_MPI_HYDRA_BOOTSTRAP=slurm',
                    'scontrol show hostnames > nodelist'
                ],
                'default_command': 'fluent 3ddp -g -t$SLURM_NPROCS -mpi=intel -cnf=$PWD/nodelist -i journal.jou',
                'mpi_flags': [],
                'recommended_partition': None,
                'partition_reason': None
            },
            'comsol': {
                'name': 'COMSOL Template',
                'description': 'Optimized for COMSOL Multiphysics finite element analysis',
                'modules': ['comsol'],
                'environment': [
                    'export SLURM_MPI_TYPE=pmi2'
                ],
                'default_command': 'comsol batch -np $SLURM_NPROCS -inputfile input.mph -outputfile output',
                'mpi_flags': [],
                'recommended_partition': None,
                'partition_reason': None
            }
        }
    
    def validate_inputs(self, data):
        """Validate user inputs"""
        errors = []
        
        # Required fields
        if not data.get('account'):
            errors.append('Account/Project handle is required')
        
        if not data.get('walltime'):
            errors.append('Walltime is required')
        
        # Validate walltime format
        walltime = data.get('walltime', '')
        if not re.match(r'^\d{1,2}:\d{2}:\d{2}$|^\d+-\d{1,2}:\d{2}:\d{2}$|^\d+$', walltime):
            errors.append('Invalid walltime format. Use HH:MM:SS, D-HH:MM:SS, or minutes')
        
        # Validate nodes and tasks
        try:
            nodes = int(data.get('nodes', 1))
            if nodes < 1:
                errors.append('Number of nodes must be at least 1')
        except ValueError:
            errors.append('Invalid number of nodes')
        
        try:
            ntasks = data.get('ntasks')
            if ntasks and int(ntasks) < 1:
                errors.append('Number of tasks must be at least 1')
        except ValueError:
            errors.append('Invalid number of tasks')
        
        return errors
    
    def generate_script(self, data):
        """Generate the sbatch script"""
        script_lines = []
        
        # Get application template
        app_template = data.get('application_template', 'general')
        template_config = self.application_templates.get(app_template, self.application_templates['general'])
        
        # Shebang
        script_lines.append('#!/bin/bash')
        script_lines.append('')
        
        # Header comment
        script_lines.append(f'# NREL HPC Job Script - {template_config["name"]}')
        script_lines.append(f'# Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        script_lines.append(f'# Job: {data.get("job_name", "my_job")}')
        script_lines.append(f'# Application: {template_config["description"]}')
        script_lines.append('')
        
        # Required SBATCH directives
        script_lines.append(f'#SBATCH --account={data["account"]}')
        script_lines.append(f'#SBATCH --time={data["walltime"]}')
        
        # Job name
        if data.get('job_name'):
            script_lines.append(f'#SBATCH --job-name={data["job_name"]}')
        
        # Partition
        if data.get('partition'):
            script_lines.append(f'#SBATCH --partition={data["partition"]}')
        
        # QOS
        if data.get('qos') and data.get('qos') != 'normal':
            script_lines.append(f'#SBATCH --qos={data["qos"]}')
        
        # Resource requests
        script_lines.append(f'#SBATCH --nodes={data.get("nodes", 1)}')
        
        if data.get('ntasks'):
            script_lines.append(f'#SBATCH --ntasks={data["ntasks"]}')
        
        if data.get('ntasks_per_node'):
            script_lines.append(f'#SBATCH --ntasks-per-node={data["ntasks_per_node"]}')
        
        if data.get('cpus_per_task'):
            script_lines.append(f'#SBATCH --cpus-per-task={data["cpus_per_task"]}')
        
        # Memory
        if data.get('memory'):
            script_lines.append(f'#SBATCH --mem={data["memory"]}')
        elif data.get('memory_per_cpu'):
            script_lines.append(f'#SBATCH --mem-per-cpu={data["memory_per_cpu"]}')
        
        # GPUs
        if data.get('gpus'):
            script_lines.append(f'#SBATCH --gpus={data["gpus"]}')
        
        # Local scratch
        if data.get('tmp_storage'):
            script_lines.append(f'#SBATCH --tmp={data["tmp_storage"]}')
        
        # Email notifications
        if data.get('email'):
            script_lines.append(f'#SBATCH --mail-user={data["email"]}')
            mail_types = []
            if data.get('mail_begin'):
                mail_types.append('BEGIN')
            if data.get('mail_end'):
                mail_types.append('END')
            if data.get('mail_fail'):
                mail_types.append('FAIL')
            if mail_types:
                script_lines.append(f'#SBATCH --mail-type={",".join(mail_types)}')
        
        # Output files
        output_file = data.get('output_file', 'slurm-%j.out')
        script_lines.append(f'#SBATCH --output={output_file}')
        
        if data.get('error_file') and data.get('error_file') != output_file:
            script_lines.append(f'#SBATCH --error={data["error_file"]}')
        
        script_lines.append('')
        
        # Job information header
        script_lines.extend([
            '# Job information',
            'echo "Job started at: $(date)"',
            'echo "Job ID: $SLURM_JOB_ID"',
            'echo "Node(s): $SLURM_JOB_NODELIST"',
            'echo "Number of nodes: $SLURM_JOB_NUM_NODES"',
            'echo "Working directory: $PWD"',
            'echo ""',
            ''
        ])
        
        # Module loading (combine template modules with user modules)
        all_modules = template_config.get('modules', [])
        if data.get('modules'):
            user_modules = [m.strip() for m in data.get('modules', '').split('\n') if m.strip()]
            all_modules.extend(user_modules)
        
        if all_modules:
            script_lines.append('# Load required modules')
            for module in all_modules:
                script_lines.append(f'module load {module}')
            script_lines.append('module list')
            script_lines.append('')
        
        # Environment setup (combine template environment with user setup)
        all_env = template_config.get('environment', [])
        if data.get('environment_setup'):
            user_env = [line.strip() for line in data.get('environment_setup', '').split('\n') if line.strip()]
            all_env.extend(user_env)
        
        if all_env:
            script_lines.append('# Environment setup')
            for line in all_env:
                script_lines.append(line)
            script_lines.append('')
        
        # Job commands
        script_lines.append('# Job execution')
        
        # Generate srun command if applicable
        srun_cmd = self._generate_srun_command(data, template_config)
        
        if data.get('commands'):
            if srun_cmd:
                script_lines.append('# MPI/Parallel execution with srun')
            for line in data.get('commands', '').split('\n'):
                line = line.strip()
                if line:
                    if srun_cmd and self._is_mpi_command(line, app_template):
                        script_lines.append(f'{srun_cmd} {line}')
                    else:
                        script_lines.append(line)
        else:
            # Use template default command if no user commands provided
            default_cmd = template_config.get('default_command', 'echo "Add your commands here"')
            if srun_cmd and self._is_mpi_command(default_cmd, app_template):
                script_lines.append(f'{srun_cmd} {default_cmd}')
            else:
                script_lines.append(default_cmd)
            
            if srun_cmd:
                script_lines.extend([
                    '',
                    '# MPI/Parallel job execution examples:',
                    f'# {srun_cmd} your_mpi_program',
                    '# For serial programs within the allocation: your_program'
                ])
        
        script_lines.append('')
        script_lines.append('echo "Job completed at: $(date)"')
        
        return '\n'.join(script_lines)
    
    def _generate_srun_command(self, data, template_config=None):
        """Generate srun command with appropriate parameters"""
        nodes = int(data.get('nodes', 1))
        ntasks = data.get('ntasks')
        ntasks_per_node = data.get('ntasks_per_node')
        cpus_per_task = data.get('cpus_per_task')
        
        # Generate srun for multi-task or multi-node jobs
        if (nodes > 1 or 
            (ntasks and int(ntasks) > 1) or 
            ntasks_per_node or 
            (cpus_per_task and int(cpus_per_task) > 1)):
            
            srun_parts = ['srun']
            
            # Add template-specific MPI flags
            if template_config and template_config.get('mpi_flags'):
                srun_parts.extend(template_config['mpi_flags'])
            
            # Add explicit parameters to srun
            if ntasks:
                srun_parts.append(f'--ntasks={ntasks}')
            if ntasks_per_node:
                srun_parts.append(f'--ntasks-per-node={ntasks_per_node}')
            if cpus_per_task:
                srun_parts.append(f'--cpus-per-task={cpus_per_task}')
                
            return ' '.join(srun_parts)
        
        return None
    
    def _is_mpi_command(self, command, app_template='general'):
        """Check if a command appears to be an MPI/parallel program"""
        # Application-specific MPI command detection
        app_mpi_indicators = {
            'general': ['python', 'mpirun', 'mpiexec', './', 'vasp', 'openfoam'],
            'gaussian': ['g16', 'g09'],  # Gaussian handles parallelization internally
            'lammps': ['lmp'],
            'ansys': ['fluent', 'ansys'],
            'comsol': ['comsol']
        }
        
        indicators = app_mpi_indicators.get(app_template, app_mpi_indicators['general'])
        cmd_lower = command.lower()
        
        # Special case: Gaussian uses g16_nrel which doesn't need srun
        if app_template == 'gaussian' and 'g16_nrel' in cmd_lower:
            return False
            
        return any(indicator in cmd_lower for indicator in indicators)

generator = JobScriptGenerator()

@app.route('/')
def index():
    """Main page with job script form"""
    return render_template('index.html', 
                         partitions=generator.partitions,
                         qos_options=generator.qos_options,
                         application_templates=generator.application_templates)

@app.route('/generate', methods=['POST'])
def generate():
    """Generate job script from form data"""
    data = request.get_json()
    
    # Validate inputs
    errors = generator.validate_inputs(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    # Generate script
    try:
        script = generator.generate_script(data)
        return jsonify({'success': True, 'script': script})
    except Exception as e:
        return jsonify({'success': False, 'errors': [str(e)]}), 500

@app.route('/download', methods=['POST'])
def download():
    """Download generated script as file"""
    data = request.get_json()
    
    # Validate and generate script
    errors = generator.validate_inputs(data)
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    try:
        script = generator.generate_script(data)
        filename = data.get('job_name', 'job') + '.sh'
        
        response = make_response(script)
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'text/plain'
        return response
    except Exception as e:
        return jsonify({'success': False, 'errors': [str(e)]}), 500

@app.route('/templates/<template_name>')
def get_template(template_name):
    """Get application template configuration"""
    template = generator.application_templates.get(template_name)
    if template:
        return jsonify({'success': True, 'template': template})
    else:
        return jsonify({'success': False, 'error': 'Template not found'}), 404

@app.route('/examples')
def examples():
    """Show example job scripts"""
    examples = {
        'cpu_debug': {
            'name': 'CPU Debug Job',
            'description': 'Simple CPU job for testing',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '00:15:00',
                'job_name': 'cpu_debug',
                'partition': 'debug',
                'nodes': '1',
                'ntasks': '1',
                'commands': 'echo "Hello from Kestrel!"\necho "Node: $SLURMD_NODENAME"'
            })
        },
        'gaussian_example': {
            'name': 'Gaussian Job',
            'description': 'Gaussian16 quantum chemistry calculation',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '02:00:00',
                'job_name': 'gaussian_job',
                'partition': 'nvme',
                'nodes': '1',
                'ntasks': '1',
                'application_template': 'gaussian',
                'commands': 'g16_nrel < benzene.gjf > benzene.log'
            })
        },
        'lammps_example': {
            'name': 'LAMMPS Job',
            'description': 'LAMMPS molecular dynamics simulation',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '04:00:00',
                'job_name': 'lammps_job',
                'partition': 'standard',
                'nodes': '2',
                'ntasks': '64',
                'ntasks_per_node': '32',
                'application_template': 'lammps'
            })
        },
        'ansys_example': {
            'name': 'ANSYS Fluent Job',
            'description': 'ANSYS Fluent CFD simulation',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '06:00:00',
                'job_name': 'fluent_job',
                'partition': 'standard',
                'nodes': '2',
                'ntasks': '104',
                'ntasks_per_node': '52',
                'application_template': 'ansys'
            })
        },
        'comsol_example': {
            'name': 'COMSOL Job',
            'description': 'COMSOL Multiphysics simulation',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '08:00:00',
                'job_name': 'comsol_job',
                'partition': 'standard',
                'nodes': '4',
                'ntasks': '32',
                'ntasks_per_node': '8',
                'cpus_per_task': '13',
                'application_template': 'comsol'
            })
        }
    }
    
    return render_template('examples.html', examples=examples)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)