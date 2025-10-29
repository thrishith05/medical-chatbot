# 🚀 Instant Render Deployment

## Quick Deploy (3 Steps)

### Step 1: Add Dataset Files

```bash
# Copy Dataset to current directory
cp -r /Users/thrishithreddy/Desktop/Dataset ./Dataset

# Add to git
git add Dataset/
git commit -m "Add medical dataset"
git push origin main
```

### Step 2: Deploy to Render

1. Go to https://render.com
2. Sign up/Login (use GitHub)
3. Click "New +" → "Web Service"
4. Click "Connect GitHub" and select this repo
5. Render auto-detects `render.yaml`
6. Click "Create Web Service"

### Step 3: Get Your URL

Wait 15-20 minutes for first build, then get:
```
https://medical-chatbot-api.onrender.com
```

---

## Alternative: No Dataset Upload

If Dataset files are too large to upload:

### Option A: Use Remote Dataset

Create a `build.sh` that downloads dataset:

```bash
#!/bin/bash
# Download or sync Dataset from cloud storage
```

### Option B: Pre-build ChromaDB Locally

Upload the chroma_db folder:

```bash
git add chroma_db/
git commit -m "Add pre-built ChromaDB"
git push
```

Then modify `render.yaml` to skip DB generation.

---

## Current Setup for Render

✅ **render.yaml** - Configured
✅ **requirements.txt** - Dependencies listed
✅ **Procfile** - Start command
✅ **runtime.txt** - Python version
✅ **app.py** - Main API

### What You Need:
1. Dataset files in repo OR
2. Upload chroma_db/ directory (112MB+)

---

## Recommended Approach

### For Fastest Deploy:

```bash
# 1. Add chroma_db to git (one-time)
git add chroma_db/
git commit -m "Add ChromaDB"
git push

# 2. Or zip it and host elsewhere
zip -r chroma_db.zip chroma_db/
# Upload to Google Drive/Dropbox and download on Render

# 3. Deploy to Render
# Go to render.com and connect repo
```

---

## Your Deployment Commands

```bash
# Stage all files
git add .

# Commit
git commit -m "Ready for Render deployment"

# Push
git push origin main

# Then go to render.com and deploy!
```

---

## Expected Result

Once deployed on Render, you'll get:

**API URL:** `https://medical-chatbot-api.onrender.com`

**Endpoints:**
- `GET https://medical-chatbot-api.onrender.com/health`
- `POST https://medical-chatbot-api.onrender.com/query`

**Test:**
```bash
curl https://medical-chatbot-api.onrender.com/health
```

