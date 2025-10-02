# 🚀 Quick Start in GitHub Codespaces

Welcome to the NREL HPC Job Script Generator!

## ⚠️ Codespace Startup Issues?

If your Codespace fails to start or has network errors, try these solutions:

### 1. **Restart the Codespace**
- Close the failed Codespace 
- Go back to the repository
- Click "Code" → "Create codespace on main" (try again)

### 2. **Use Different Region**
- When creating Codespace, click "Configure and create codespace"
- Choose a different region (US West, Europe, etc.)

### 3. **Use Minimal Mode** (if network is slow)
```bash
./start-minimal.sh
```

## Starting the Application

### Option 1: Standard Start (Recommended)
```bash
./start.sh
```

### Option 2: Minimal Start (for slow networks)
```bash
./start-minimal.sh
```

### Option 3: Manual Start
```bash
# Install dependencies (if needed)
pip install flask werkzeug jinja2

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