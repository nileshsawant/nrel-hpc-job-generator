# 🚀 Quick Start in GitHub Codespaces

Welcome to the NREL HPC Job Script Generator!

## Starting the Application

### Option 1: Use the Start Script (Recommended)
```bash
./start.sh
```

### Option 2: Manual Start
```bash
# Install dependencies (if needed)
pip install -r requirements.txt

# Start the app
python app.py
```

## Accessing the App

1. Once the app starts, you'll see output like:
   ```
   * Running on http://127.0.0.1:5000
   * Running on http://0.0.0.0:5000
   ```

2. VS Code will show a popup asking to open the port in browser - **click "Open in Browser"**

3. Or manually click the **"PORTS"** tab at the bottom and click the 🌐 icon next to port 5000

## Troubleshooting

**Port 5000 busy?**
- The script will automatically use port 5001
- Look for the new port number in the PORTS tab

**App not loading?**
- Make sure to click "Open in Browser" when prompted
- Check the PORTS tab and click the correct port

**Need help?**
- The app generates Slurm job scripts for NREL HPC systems
- Fill out the form and download your `.sh` script
- Submit to Kestrel with: `sbatch your_script.sh`

---

🎯 **Ready to generate job scripts!** 🎯