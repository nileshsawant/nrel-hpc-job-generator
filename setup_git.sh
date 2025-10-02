#!/bin/bash

# NREL HPC Job Script Generator - Git Setup Script

echo "🚀 Setting up Git repository for NREL HPC Job Script Generator..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Flask
instance/
.webassets-cache

# Environment variables
.env
.env.local

# Logs
*.log
EOL
    echo "✅ .gitignore created"
fi

# Add all files
git add .

# Initial commit
if git rev-parse --verify HEAD >/dev/null 2>&1; then
    echo "✅ Repository already has commits"
else
    git commit -m "Initial commit: NREL HPC Job Script Generator

- Flask web application for generating Slurm batch scripts
- Interactive form with validation
- Real-time script preview
- Example scripts for common job types
- Optimized for NREL Kestrel HPC system
- Multiple deployment options configured"
    echo "✅ Initial commit created"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Create a GitHub repository at: https://github.com/new"
echo "2. Run these commands with your repository URL:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/nrel-hpc-job-generator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Then follow the deployment guide in DEPLOYMENT_GUIDE.md"
echo ""
echo "📁 Your project is ready at: $(pwd)"