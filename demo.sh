#!/bin/bash
# Demo script for NREL HPC Job Script Generator CLI

echo "=== NREL HPC Job Script Generator CLI Demo ==="
echo ""

echo "1. Basic job script generation:"
echo "Command: python3 generate_job.py --account csc000 --time 01:00:00 --job-name demo_job"
echo ""
python3 generate_job.py --account csc000 --time 01:00:00 --job-name demo_job
echo ""
echo "=================================================================="
echo ""

echo "2. More complex job with resources and modules:"
echo "Command: python3 generate_job.py --account csc000 --time 2:00:00 --job-name parallel_demo --nodes 2 --ntasks 64 --memory 100GB --modules python/3.9 gcc/8.4.0 --commands 'echo Hello from parallel job' 'python -c \"import multiprocessing; print(f\"CPUs: {multiprocessing.cpu_count()}\")\"'"
echo ""
python3 generate_job.py \
  --account csc000 \
  --time 2:00:00 \
  --job-name parallel_demo \
  --nodes 2 \
  --ntasks 64 \
  --memory 100GB \
  --modules python/3.9 gcc/8.4.0 \
  --commands 'echo "Hello from parallel job"' 'python -c "import multiprocessing; print(f\"CPUs: {multiprocessing.cpu_count()}\")"'

echo ""
echo "=================================================================="
echo ""

echo "3. GPU job example:"
echo "Command: python3 generate_job.py --account csc000 --time 30 --partition debug --gpus 1 --modules cuda/11.8 --commands nvidia-smi"
echo ""
python3 generate_job.py \
  --account csc000 \
  --time 30 \
  --partition debug \
  --gpus 1 \
  --modules cuda/11.8 \
  --commands nvidia-smi

echo ""
echo "=================================================================="
echo ""

echo "4. Save to file example:"
echo "Command: python3 generate_job.py --account csc000 --time 01:00:00 --job-name saved_job --save demo_job.sh"
echo ""
python3 generate_job.py \
  --account csc000 \
  --time 01:00:00 \
  --job-name saved_job \
  --save demo_job.sh

echo "Generated file contents:"
cat demo_job.sh

echo ""
echo "=================================================================="
echo ""

echo "Demo complete! Try running:"
echo "  python3 generate_job.py --interactive"
echo "  python3 generate_job.py --help"