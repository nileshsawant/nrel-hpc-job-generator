# Deployment Guide - NREL HPC Job Script Generator

## Option 1: GitHub Codespaces (Recommended)

### Setup Instructions:
1. **Push to GitHub**: Upload your repository to GitHub
2. **Configure Codespaces**: Add development container configuration
3. **Users Access**: Users open Codespaces and run the app in their browser

### Benefits:
- ✅ Free for users with GitHub accounts
- ✅ No server maintenance required
- ✅ Users get their own isolated environment
- ✅ Perfect for NREL researchers with GitHub access

---

## Option 2: Heroku Deployment

### Setup Instructions:
1. Create Heroku account and install Heroku CLI
2. Add Procfile for web process
3. Deploy with git push
4. Share public URL with users

### Benefits:
- ✅ Always accessible via web URL
- ✅ No GitHub account required for users
- ✅ Custom domain possible
- ⚠️  Free tier sleeps after 30 min inactivity

---

## Option 3: Railway Deployment

### Setup Instructions:
1. Connect GitHub repository to Railway
2. Automatic deployment on push
3. Get public URL

### Benefits:
- ✅ Modern platform with better free tier
- ✅ Automatic deployments
- ✅ Good performance
- ✅ No sleep issues

---

## Option 4: Local Network Deployment

### For NREL Internal Use:
- Deploy on NREL servers/VM
- Integrate with NREL authentication
- Control access through VPN/network

---

## Files Needed for Deployment

Each deployment option requires different configuration files. The generator will create the appropriate files based on your choice.