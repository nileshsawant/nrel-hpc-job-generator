# NREL HPC Job Script Generator

This is a Python Flask web application for generating NREL HPC Slurm job scripts with an interactive web interface.

## Project Status
- [x] Verify that the copilot-instructions.md file in the .github directory is created.
- [x] Clarify Project Requirements - Python Flask web app for NREL HPC job script generation
- [x] Scaffold the Project - Created Flask app, templates, and core functionality  
- [x] Customize the Project - Implemented job script generator with NREL-specific features
- [x] Install Required Extensions - No extensions needed for this project
- [x] Compile the Project - Python environment configured and Flask dependencies installed
- [x] Create and Run Task - Flask development server started successfully
- [x] Launch the Project - Application running on http://localhost:5000
- [x] Ensure Documentation is Complete - README.md created with comprehensive documentation

## Project Details
- **Type**: Python Flask web application
- **Purpose**: Generate NREL HPC Slurm job scripts
- **Features**: Interactive web form, job script templates, validation, examples
- **Target System**: NREL Kestrel HPC system

## Usage Instructions

The application is now running and accessible at:
- **Local**: http://localhost:5000 or http://127.0.0.1:5000
- **Network**: http://10.40.6.102:5000

### Features Available:
1. **Job Script Generator**: Main form with all NREL HPC parameters
2. **Real-time Validation**: Input checking and error reporting  
3. **Live Preview**: Generated script updates as you type
4. **Download Functionality**: Save scripts as .sh files
5. **Example Library**: Pre-built templates for common job types

### Development Commands:
- Start server: `python app.py` (already running)
- Install dependencies: `pip install -r requirements.txt` (completed)
- Activate environment: `source .venv/bin/activate`

## Project Structure Completed:
- `app.py` - Flask application with job script generation logic
- `templates/` - HTML templates with Bootstrap styling
- `requirements.txt` - Python dependencies
- `README.md` - Complete documentation
- `.venv/` - Python virtual environment (configured)
- `.github/copilot-instructions.md` - This file

The project is fully functional and ready for use!