# 🔧 Troubleshooting Guide

## GitHub Codespaces Issues

### Problem: App doesn't start automatically
**Solution:** 
```bash
./start.sh
```

### Problem: Port 5000 is busy
**Solution:** The start script will automatically use port 5001. Look for the message:
```
⚠️  Port 5000 is busy, using port 5001...
🌐 App will be available at: http://localhost:5001
```

### Problem: Can't access the web interface
**Solutions:**
1. Click "Open in Browser" when VS Code prompts
2. Go to the **PORTS** tab at the bottom of VS Code
3. Click the 🌐 globe icon next to the port number
4. Or click the port number to copy the URL

### Problem: Dependencies not installed
**Solution:**
```bash
pip install -r requirements.txt
python app.py
```

### Problem: Python not found
**Solution:** The Codespace should have Python pre-installed. Try:
```bash
which python
python --version
```

## Local Development Issues

### Problem: Port 5000 already in use (macOS)
**Solutions:**
1. **Kill existing processes:**
   ```bash
   lsof -i :5000
   kill -9 [PID_NUMBER]
   ```

2. **Use different port:**
   ```bash
   PORT=5001 python app.py
   ```

3. **Disable macOS AirPlay Receiver:**
   - System Preferences → General → AirDrop & Handoff
   - Turn off "AirPlay Receiver"

### Problem: Flask not found
**Solution:**
```bash
# Activate virtual environment
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Common Usage Issues

### Problem: Generated script has errors
**Check:**
- Account name is correct (your NREL project handle)
- Walltime format: `HH:MM:SS` or `D-HH:MM:SS`
- Resource requests are reasonable for your job

### Problem: Download not working
**Solutions:**
- Check browser popup blockers
- Right-click "Download" → "Save link as..."
- Copy the script text manually

### Problem: Form validation errors
**Common fixes:**
- Account field cannot be empty
- Walltime must be in correct format
- Node count must be at least 1
- Numeric fields should contain only numbers

## Need More Help?

1. **Check the examples** in the Examples tab
2. **Review NREL HPC docs**: https://nrel.github.io/HPC/
3. **Verify script locally** before submitting to queue

---

💡 **Pro Tip:** Always test your job scripts with a short walltime in the `debug` partition first!