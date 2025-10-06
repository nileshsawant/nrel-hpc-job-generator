#!/usr/bin/env python3
"""
NREL HPC Job Script Generator - Command Line Interface
Generate Slurm batch scripts for NREL Kestrel HPC system from the command line.
"""

import argparse
import sys
from datetime import datetime
import re
import os

class JobScriptCLI:
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
        
        self.qos_options = ['normal', 'high', 'standby']

    def create_parser(self):
        parser = argparse.ArgumentParser(
            description='Generate NREL HPC Slurm job scripts',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --account csc000 --time 01:00:00 --job-name my_job
  %(prog)s -A csc000 -t 2:00:00 -J test --nodes 2 --ntasks 64
  %(prog)s --account csc000 --time 30 --partition debug --gpus 1
  %(prog)s --interactive  # Interactive mode
            """
        )
        
        # Mode selection
        parser.add_argument('--interactive', '-i', action='store_true',
                          help='Run in interactive mode')
        
        # Required parameters
        parser.add_argument('--account', '-A', type=str,
                          help='Account/Project handle (required)')
        parser.add_argument('--time', '-t', type=str,
                          help='Walltime: HH:MM:SS, D-HH:MM:SS, or minutes (required)')
        
        # Job identification
        parser.add_argument('--job-name', '-J', type=str,
                          help='Job name')
        parser.add_argument('--partition', '-p', choices=list(self.partitions.keys()),
                          help='Partition: ' + ', '.join(self.partitions.keys()))
        parser.add_argument('--qos', choices=self.qos_options,
                          help='Quality of Service: ' + ', '.join(self.qos_options))
        
        # Resource requests
        parser.add_argument('--nodes', '-N', type=int, default=1,
                          help='Number of nodes (default: 1)')
        parser.add_argument('--ntasks', '-n', type=int,
                          help='Total number of MPI tasks/ranks')
        parser.add_argument('--ntasks-per-node', '--ranks-per-node', type=int,
                          help='Number of MPI ranks per node')
        parser.add_argument('--cpus-per-task', '--threads-per-rank', '-c', type=int,
                          help='Number of CPUs/threads per MPI rank')
        parser.add_argument('--memory', '--mem', type=str,
                          help='Memory per node (e.g., 50GB)')
        parser.add_argument('--memory-per-cpu', type=str,
                          help='Memory per CPU (e.g., 2GB)')
        parser.add_argument('--gpus', '-G', type=int,
                          help='Number of GPUs')
        parser.add_argument('--tmp', type=str,
                          help='Local scratch storage (e.g., 100GB)')
        
        # Email notifications
        parser.add_argument('--mail-user', type=str,
                          help='Email address for notifications')
        parser.add_argument('--mail-type', type=str, default='END,FAIL',
                          help='Mail types: BEGIN, END, FAIL, ALL (default: END,FAIL)')
        
        # Output files
        parser.add_argument('--output', '-o', type=str, default='slurm-%j.out',
                          help='Output file (default: slurm-%%j.out)')
        parser.add_argument('--error', '-e', type=str,
                          help='Error file (default: same as output)')
        
        # Job setup
        parser.add_argument('--modules', type=str, nargs='*',
                          help='Modules to load (space-separated)')
        parser.add_argument('--commands', type=str, nargs='*',
                          help='Commands to execute (space-separated)')
        parser.add_argument('--script-file', type=str,
                          help='File containing job commands')
        
        # Output options
        parser.add_argument('--save', '-s', type=str,
                          help='Save script to file')
        parser.add_argument('--submit', action='store_true',
                          help='Submit job after generating script')
        
        return parser

    def validate_args(self, args):
        """Validate command line arguments"""
        errors = []
        
        if not args.interactive:
            if not args.account:
                errors.append('--account is required')
            if not args.time:
                errors.append('--time is required')
        
        if args.time:
            if not re.match(r'^\d{1,2}:\d{2}:\d{2}$|^\d+-\d{1,2}:\d{2}:\d{2}$|^\d+$', args.time):
                errors.append('Invalid walltime format. Use HH:MM:SS, D-HH:MM:SS, or minutes')
        
        if args.nodes and args.nodes < 1:
            errors.append('Number of nodes must be at least 1')
        
        return errors

    def interactive_mode(self):
        """Run interactive mode to collect job parameters"""
        print("=== NREL HPC Job Script Generator ===")
        print("Interactive Mode - Press Enter for defaults\n")
        
        # Required parameters
        account = input("Account/Project handle (required): ").strip()
        while not account:
            account = input("Account is required. Please enter: ").strip()
        
        walltime = input("Walltime (HH:MM:SS or minutes, required): ").strip()
        while not walltime or not re.match(r'^\d{1,2}:\d{2}:\d{2}$|^\d+-\d{1,2}:\d{2}:\d{2}$|^\d+$', walltime):
            walltime = input("Invalid format. Enter walltime (HH:MM:SS or minutes): ").strip()
        
        # Optional parameters
        job_name = input("Job name [my_job]: ").strip() or "my_job"
        
        print(f"Partitions: {', '.join(self.partitions.keys())}")
        partition = input("Partition [default]: ").strip()
        if partition and partition not in self.partitions:
            print(f"Warning: {partition} not in known partitions")
        
        nodes = input("Number of nodes [1]: ").strip() or "1"
        try:
            nodes = int(nodes)
        except ValueError:
            nodes = 1
        
        print("\\nMPI Configuration (leave blank for non-MPI jobs):")
        ntasks = input("Total MPI ranks/tasks [optional]: ").strip()
        if ntasks:
            try:
                ntasks = int(ntasks)
            except ValueError:
                ntasks = None
        else:
            ntasks = None
        
        ntasks_per_node = input("MPI ranks per node [optional]: ").strip()
        if ntasks_per_node:
            try:
                ntasks_per_node = int(ntasks_per_node)
            except ValueError:
                ntasks_per_node = None
        else:
            ntasks_per_node = None
            
        cpus_per_task = input("Threads per MPI rank (CPUs per task) [optional]: ").strip()
        if cpus_per_task:
            try:
                cpus_per_task = int(cpus_per_task)
            except ValueError:
                cpus_per_task = None
        else:
            cpus_per_task = None
        
        gpus = input("Number of GPUs [optional]: ").strip()
        if gpus:
            try:
                gpus = int(gpus)
            except ValueError:
                gpus = None
        else:
            gpus = None
        
        memory = input("Memory per node (e.g., 50GB) [optional]: ").strip() or None
        email = input("Email for notifications [optional]: ").strip() or None
        
        modules = input("Modules to load (comma-separated) [optional]: ").strip()
        modules = [m.strip() for m in modules.split(',')] if modules else []
        
        commands = input("Job commands (comma-separated) [optional]: ").strip()
        commands = [c.strip() for c in commands.split(',')] if commands else []
        
        # Create args object
        class Args:
            pass
        
        args = Args()
        args.interactive = True
        args.account = account
        args.time = walltime
        args.job_name = job_name
        args.partition = partition if partition else None
        args.qos = None
        args.nodes = nodes
        args.ntasks = ntasks
        args.ntasks_per_node = ntasks_per_node
        args.cpus_per_task = cpus_per_task
        args.memory = memory
        args.memory_per_cpu = None
        args.gpus = gpus
        args.tmp = None
        args.mail_user = email
        args.mail_type = 'END,FAIL' if email else None
        args.output = 'slurm-%j.out'
        args.error = None
        args.modules = modules
        args.commands = commands
        args.script_file = None
        args.save = None
        args.submit = False
        
        return args

    def generate_script(self, args):
        """Generate the job script"""
        lines = []
        
        # Shebang
        lines.append('#!/bin/bash')
        lines.append('')
        
        # Header
        lines.append('# NREL HPC Job Script')
        lines.append(f'# Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        lines.append(f'# Job: {args.job_name or "my_job"}')
        lines.append('')
        
        # Required SBATCH directives
        lines.append(f'#SBATCH --account={args.account}')
        lines.append(f'#SBATCH --time={args.time}')
        
        # Optional directives
        if args.job_name:
            lines.append(f'#SBATCH --job-name={args.job_name}')
        
        if args.partition:
            lines.append(f'#SBATCH --partition={args.partition}')
        
        if args.qos and args.qos != 'normal':
            lines.append(f'#SBATCH --qos={args.qos}')
        
        # Resource requests
        lines.append(f'#SBATCH --nodes={args.nodes}')
        
        if args.ntasks:
            lines.append(f'#SBATCH --ntasks={args.ntasks}')
        
        if args.ntasks_per_node:
            lines.append(f'#SBATCH --ntasks-per-node={args.ntasks_per_node}')
        
        if args.cpus_per_task:
            lines.append(f'#SBATCH --cpus-per-task={args.cpus_per_task}')
        
        if args.memory:
            lines.append(f'#SBATCH --mem={args.memory}')
        elif args.memory_per_cpu:
            lines.append(f'#SBATCH --mem-per-cpu={args.memory_per_cpu}')
        
        if args.gpus:
            lines.append(f'#SBATCH --gpus={args.gpus}')
        
        if args.tmp:
            lines.append(f'#SBATCH --tmp={args.tmp}')
        
        # Email notifications
        if args.mail_user:
            lines.append(f'#SBATCH --mail-user={args.mail_user}')
            if args.mail_type:
                lines.append(f'#SBATCH --mail-type={args.mail_type}')
        
        # Output files
        lines.append(f'#SBATCH --output={args.output}')
        if args.error and args.error != args.output:
            lines.append(f'#SBATCH --error={args.error}')
        
        lines.append('')
        
        # Job information
        lines.extend([
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
        if args.modules:
            lines.append('# Load required modules')
            for module in args.modules:
                if module:
                    lines.append(f'module load {module}')
            lines.append('')
        
        # Job commands
        lines.append('# Job execution')
        
        # Generate srun command if applicable
        srun_cmd = self._generate_srun_command(args)
        
        if args.commands:
            if srun_cmd:
                lines.append('# MPI/Parallel execution with srun')
            for command in args.commands:
                if command:
                    if srun_cmd and self._is_mpi_command(command):
                        lines.append(f'{srun_cmd} {command}')
                    else:
                        lines.append(command)
        elif args.script_file:
            if os.path.exists(args.script_file):
                if srun_cmd:
                    lines.append('# MPI/Parallel execution with srun')
                with open(args.script_file, 'r') as f:
                    for line in f:
                        line = line.rstrip()
                        if line and srun_cmd and self._is_mpi_command(line):
                            lines.append(f'{srun_cmd} {line}')
                        else:
                            lines.append(line)
            else:
                lines.append(f'# Script file {args.script_file} not found')
                lines.append('echo "Script file not found"')
        else:
            if srun_cmd:
                lines.extend([
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
                lines.extend([
                    '# Add your job commands here',
                    'echo "Replace this with your actual job commands"'
                ])
        
        lines.append('')
        lines.append('echo "Job completed at: $(date)"')
        
        return '\n'.join(lines)
    
    def _generate_srun_command(self, args):
        """Generate srun command with appropriate parameters"""
        nodes = args.nodes
        ntasks = args.ntasks
        ntasks_per_node = args.ntasks_per_node
        cpus_per_task = args.cpus_per_task
        
        # Generate srun for multi-task or multi-node jobs
        if (nodes > 1 or 
            (ntasks and ntasks > 1) or 
            ntasks_per_node or 
            (cpus_per_task and cpus_per_task > 1)):
            
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

    def run(self):
        """Main CLI entry point"""
        parser = self.create_parser()
        
        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            return 1
        
        args = parser.parse_args()
        
        # Interactive mode
        if args.interactive:
            args = self.interactive_mode()
        
        # Validate arguments
        errors = self.validate_args(args)
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  - {error}")
            return 1
        
        # Generate script
        script = self.generate_script(args)
        
        # Output handling
        if args.save:
            with open(args.save, 'w') as f:
                f.write(script)
            print(f"Job script saved to: {args.save}")
            
            # Make executable
            os.chmod(args.save, 0o755)
            
            # Submit if requested
            if args.submit:
                import subprocess
                try:
                    result = subprocess.run(['sbatch', args.save], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"Job submitted: {result.stdout.strip()}")
                    else:
                        print(f"Submission failed: {result.stderr.strip()}")
                except FileNotFoundError:
                    print("Error: sbatch command not found. Are you on an HPC system?")
        else:
            # Print to stdout
            print(script)
        
        return 0

def main():
    """Entry point for the CLI"""
    try:
        cli = JobScriptCLI()
        return cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())