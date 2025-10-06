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
        
        # Shebang
        script_lines.append('#!/bin/bash')
        script_lines.append('')
        
        # Header comment
        script_lines.append(f'# NREL HPC Job Script')
        script_lines.append(f'# Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        script_lines.append(f'# Job: {data.get("job_name", "my_job")}')
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
        
        # Module loading
        if data.get('modules'):
            script_lines.append('# Load required modules')
            for module in data.get('modules', '').split('\n'):
                module = module.strip()
                if module:
                    script_lines.append(f'module load {module}')
            script_lines.append('')
        
        # Environment setup
        if data.get('environment_setup'):
            script_lines.append('# Environment setup')
            for line in data.get('environment_setup', '').split('\n'):
                line = line.strip()
                if line:
                    script_lines.append(line)
            script_lines.append('')
        
        # Job commands
        script_lines.append('# Job execution')
        
        # Generate srun command if applicable
        srun_cmd = self._generate_srun_command(data)
        
        if data.get('commands'):
            if srun_cmd:
                script_lines.append('# MPI/Parallel execution with srun')
            for line in data.get('commands', '').split('\n'):
                line = line.strip()
                if line:
                    if srun_cmd and self._is_mpi_command(line):
                        script_lines.append(f'{srun_cmd} {line}')
                    else:
                        script_lines.append(line)
        else:
            if srun_cmd:
                script_lines.extend([
                    '# MPI/Parallel job execution',
                    f'# Use srun for MPI programs: {srun_cmd} your_mpi_program',
                    '# For serial programs within the allocation: your_program',
                    '',
                    '# Example MPI command:',
                    f'# {srun_cmd} python your_parallel_script.py',
                    '',
                    'echo "Add your MPI/parallel job commands here"'
                ])
            else:
                script_lines.extend([
                    '# Add your job commands here',
                    'echo "Replace this with your actual job commands"'
                ])
        
        script_lines.append('')
        script_lines.append('echo "Job completed at: $(date)"')
        
        return '\n'.join(script_lines)
    
    def _generate_srun_command(self, data):
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
            
            # Add explicit parameters to srun
            if ntasks:
                srun_parts.append(f'--ntasks={ntasks}')
            if ntasks_per_node:
                srun_parts.append(f'--ntasks-per-node={ntasks_per_node}')
            if cpus_per_task:
                srun_parts.append(f'--cpus-per-task={cpus_per_task}')
                
            return ' '.join(srun_parts)
        
        return None
    
    def _is_mpi_command(self, command):
        """Check if a command appears to be an MPI/parallel program"""
        # Commands that typically benefit from srun
        mpi_indicators = ['python', 'mpirun', 'mpiexec', './', 'vasp', 'lammps', 'openfoam']
        cmd_lower = command.lower()
        return any(indicator in cmd_lower for indicator in mpi_indicators)

generator = JobScriptGenerator()

@app.route('/')
def index():
    """Main page with job script form"""
    return render_template('index.html', 
                         partitions=generator.partitions,
                         qos_options=generator.qos_options)

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
        'gpu_job': {
            'name': 'GPU Job',
            'description': 'Job requesting GPU resources',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '01:00:00',
                'job_name': 'gpu_job',
                'partition': 'standard',
                'nodes': '1',
                'gpus': '1',
                'commands': 'nvidia-smi\necho "GPU job running on $SLURMD_NODENAME"'
            })
        },
        'mpi_job': {
            'name': 'MPI Job',
            'description': 'Multi-node MPI job',
            'script': generator.generate_script({
                'account': 'your_project',
                'walltime': '02:00:00',
                'job_name': 'mpi_job',
                'partition': 'standard',
                'nodes': '4',
                'ntasks': '128',
                'ntasks_per_node': '32',
                'modules': 'gcc\nopenmpi',
                'commands': 'mpirun ./my_mpi_program'
            })
        }
    }
    
    return render_template('examples.html', examples=examples)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)