#!/bin/bash
# NREL HPC Job Script Generator - Installation Script
# This script sets up the CLI tool for easy use

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}NREL HPC Job Script Generator - Setup${NC}"
echo "============================================"

# Check if we're on a supported system
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not found${NC}"
    exit 1
fi

# Check if on HPC system (optional)
if command -v sbatch &> /dev/null; then
    echo -e "${GREEN}✓ SLURM detected - full functionality available${NC}"
else
    echo -e "${YELLOW}⚠ SLURM not detected - script generation only${NC}"
fi

# Create local bin directory if it doesn't exist
mkdir -p ~/bin

# Copy the script to user's bin directory
if [ -f "generate_job.py" ]; then
    cp generate_job.py ~/bin/
    chmod +x ~/bin/generate_job.py
    
    # Create a convenient alias
    cat > ~/bin/nrel-jobgen << 'EOF'
#!/bin/bash
python3 ~/bin/generate_job.py "$@"
EOF
    chmod +x ~/bin/nrel-jobgen
    
    echo -e "${GREEN}✓ Installed to ~/bin/generate_job.py${NC}"
    echo -e "${GREEN}✓ Created alias: ~/bin/nrel-jobgen${NC}"
else
    echo -e "${RED}Error: generate_job.py not found in current directory${NC}"
    exit 1
fi

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}NOTE: ~/bin is not in your PATH${NC}"
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    echo "Or run directly with: ~/bin/nrel-jobgen"
else
    echo -e "${GREEN}✓ ~/bin is in PATH - you can use 'nrel-jobgen' command${NC}"
fi

echo ""
echo -e "${BLUE}Installation complete!${NC}"
echo ""
echo "Usage examples:"
echo "  nrel-jobgen --interactive"
echo "  nrel-jobgen --account csc000 --time 01:00:00 --job-name test"
echo "  nrel-jobgen --help"
echo ""
echo "For help: nrel-jobgen --help"