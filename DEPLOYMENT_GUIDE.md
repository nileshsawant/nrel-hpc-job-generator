# 🚀 Deployment Guide - NREL HPC Job Script Generator

This guide shows you how to deploy the NREL HPC Job Script Generator so users can access it online through various platforms.

## 🎯 Quick Summary

| Platform | Difficulty | Cost | Best For |
|----------|------------|------|----------|
| **GitHub Codespaces** | ⭐ Easy | Free* | NREL researchers with GitHub |
| **Heroku** | ⭐⭐ Medium | Free/Paid | Public access |
| **Railway** | ⭐ Easy | Free/Paid | Modern deployment |
| **Render** | ⭐ Easy | Free/Paid | Reliable hosting |

*Free with GitHub Pro/Team accounts (available to NREL)

---

## 🏆 Recommended: GitHub Codespaces

**Best for NREL users** - No server setup needed, users get isolated environments.

### Setup Steps:

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: NREL HPC Job Script Generator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/nrel-hpc-job-generator.git
   git push -u origin main
   ```

2. **Share with Users**:
   - Send users this link: `https://github.com/YOUR_USERNAME/nrel-hpc-job-generator`
   - Users click "Code" → "Create codespace on main"
   - App automatically starts at `http://localhost:5000`

### User Experience:
```
1. User visits GitHub repo
2. Clicks "Open in Codespace" 
3. Codespace loads with app running
4. User accesses job generator in browser tab
```

---

## 🌐 Option 2: Heroku (Public Web App)

**Best for public access** - Always available at a web URL.

### Setup Steps:

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Login
   heroku login
   ```

2. **Deploy**:
   ```bash
   # Create Heroku app
   heroku create nrel-hpc-job-generator
   
   # Deploy
   git push heroku main
   
   # Open app
   heroku open
   ```

3. **Share URL**: `https://nrel-hpc-job-generator.herokuapp.com`

### Benefits:
- ✅ Always accessible via web URL
- ✅ No GitHub account needed for users  
- ✅ Custom domain possible
- ⚠️ Free tier sleeps after 30 min (wakes up quickly)

---

## ⚡ Option 3: Railway (Modern Platform)

**Best performance and reliability** for continuous use.

### Setup Steps:

1. **Visit Railway**: https://railway.app
2. **Connect GitHub**: Link your repository
3. **Deploy**: Automatic deployment from GitHub
4. **Get URL**: Railway provides public URL

### Benefits:
- ✅ Excellent free tier (no sleeping)
- ✅ Automatic deployments on GitHub push
- ✅ Great performance
- ✅ Built-in monitoring

---

## 🛠️ Option 4: Render

Another excellent modern platform.

### Setup Steps:

1. **Visit Render**: https://render.com
2. **Connect GitHub repo**
3. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. **Deploy**

---

## 🏢 Option 5: NREL Internal Hosting

For official NREL deployment, contact NREL IT about hosting on:
- NREL internal servers
- NREL cloud infrastructure  
- Integration with NREL authentication systems

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Updated `requirements.txt` with all dependencies
- [ ] Added environment variable support (✅ already done)
- [ ] Tested the app locally works correctly
- [ ] Created README with usage instructions (✅ already done)
- [ ] Added appropriate `.gitignore` file

---

## 🎯 Recommendation for NREL

**For NREL HPC users, I recommend this approach:**

1. **Primary**: Use **GitHub Codespaces** for researchers with GitHub access
2. **Secondary**: Deploy to **Railway** for a permanent public URL
3. **Future**: Work with NREL IT for official internal hosting

This gives you both immediate availability and a path to official deployment.

---

## 🚀 Ready to Deploy?

Choose your preferred option above and follow the steps. The app is already configured for all these platforms!

**Need help?** The configuration files are already created:
- `.devcontainer/devcontainer.json` - GitHub Codespaces
- `Procfile` - Heroku  
- `Dockerfile` - Any container platform
- `railway.toml` - Railway specific config