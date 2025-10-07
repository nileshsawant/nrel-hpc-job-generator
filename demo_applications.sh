#!/bin/bash

# Demo script showing application-specific templates for NREL HPC Job Script Generator
# This script demonstrates the enhanced functionality with Gaussian, LAMMPS, ANSYS, and COMSOL templates

echo "=== NREL HPC Job Script Generator - Application Templates Demo ==="
echo

echo "1. List available application templates:"
echo "----------------------------------------"
python3 generate_job.py --list-templates
echo

echo "2. Generate Gaussian job script:"
echo "--------------------------------"
python3 generate_job.py \
    --template gaussian \
    --account csc000 \
    --time 02:00:00 \
    --job-name gaussian_benzene \
    --partition nvme \
    --nodes 1 \
    --ntasks 1 \
    --commands "g16_nrel < benzene.gjf > benzene.log" \
    --save gaussian_job.sh
echo "Generated: gaussian_job.sh"
echo

echo "3. Generate LAMMPS MPI job script:"
echo "----------------------------------"
python3 generate_job.py \
    --template lammps \
    --account csc000 \
    --time 04:00:00 \
    --job-name lammps_md \
    --partition hbw \
    --nodes 4 \
    --ntasks 128 \
    --ntasks-per-node 32 \
    --save lammps_job.sh
echo "Generated: lammps_job.sh"
echo

echo "4. Generate ANSYS Fluent job script:"
echo "------------------------------------"
python3 generate_job.py \
    --template ansys \
    --account csc000 \
    --time 06:00:00 \
    --job-name fluent_cfd \
    --partition standard \
    --nodes 2 \
    --ntasks 104 \
    --ntasks-per-node 52 \
    --commands "fluent 3ddp -g -t\$SLURM_NPROCS -mpi=intel -cnf=\$PWD/nodelist -i simulation.jou" \
    --save ansys_job.sh
echo "Generated: ansys_job.sh"
echo

echo "5. Generate COMSOL hybrid MPI+OpenMP job script:"
echo "------------------------------------------------"
python3 generate_job.py \
    --template comsol \
    --account csc000 \
    --time 08:00:00 \
    --job-name comsol_multiphysics \
    --partition standard \
    --nodes 4 \
    --ntasks 32 \
    --ntasks-per-node 8 \
    --cpus-per-task 13 \
    --commands "comsol batch -mpibootstrap slurm -inputfile model.mph -outputfile results" \
    --save comsol_job.sh
echo "Generated: comsol_job.sh"
echo

echo "6. Example of interactive mode for Gaussian:"
echo "--------------------------------------------"
echo "Try running: python3 generate_job.py --interactive"
echo "And select 'gaussian' as the template for guided setup"
echo

echo "Generated job scripts:"
ls -la *_job.sh 2>/dev/null || echo "No job scripts found. Run the individual commands above."
echo

echo "=== Demo Complete ==="
echo "You can now:"
echo "1. Review the generated job scripts"
echo "2. Submit them with: sbatch script_name.sh"
echo "3. Try interactive mode: python3 generate_job.py --interactive"
echo "4. Use the Flask web interface: python3 app.py"
echo "5. Use the enhanced standalone HTML: open standalone_enhanced.html"