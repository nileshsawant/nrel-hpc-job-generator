from flask import Flask, render_template, request, jsonify, make_response
from datetime import datetime, timedelta
import re

app = Flask(__name__)

class JobScriptGenerator:
    """Generator for NREL HPC Slurm job scripts"""
    
    def __init__(self):
        self.partitions = {
            'debug': {'max_time': '00:30:00', 'description': 'Debug partition (30 min max)'},
            'short': {'max_time': '04:00:00', 'description': 'Short jobs (4 hours max)'},
            'standard': {'max_time': '24:00:00', 'description': 'Standard jobs (24 hours max)'},
            'long': {'max_time': '48:00:00', 'description': 'Long jobs (48 hours max)'}
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
        if data.get('commands'):
            for line in data.get('commands', '').split('\n'):
                line = line.strip()
                if line:
                    script_lines.append(line)
        else:
            script_lines.extend([
                '# Add your job commands here',
                'echo "Replace this with your actual job commands"'
            ])
        
        script_lines.append('')
        script_lines.append('echo "Job completed at: $(date)"')
        
        return '\n'.join(script_lines)

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