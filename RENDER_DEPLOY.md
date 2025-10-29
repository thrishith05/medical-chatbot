# Render Deployment Guide

## ⚠️ Critical Issue: ChromaDB Too Large

Your `chroma_db` directory is **112MB** and will grow to 500MB+ during build.

### Solutions:

#### Option 1: Generate DB on Render (Recommended)
Let Render build the vector database during deployment.

**Pros:**
- No need to upload large files
- Git-friendly (small repo)

**Cons:**
- First deploy takes 10-20 minutes
- Need to upload Dataset files or reference remote source

#### Option 2: Use External ChromaDB
Use a cloud ChromaDB service or S3 storage.

#### Option 3: Docker with Large Files
Use Docker build with layers (slower but works).

---

## Ready-to-Deploy Setup

I've configured everything for Render deployment.

### Files Created/Updated:
- ✅ `render.yaml` - Updated for Python runtime
- ✅ `Procfile` - Start command
- ✅ `runtime.txt` - Python version
- ✅ `.dockerignore` - Already configured

### What You Need to Do:

#### Step 1: Upload Dataset to GitHub

If you have Dataset files locally:
```bash
# Copy Dataset if not in git
cp -r /Users/thrishithreddy/Desktop/Dataset ./Dataset

# Add to git (if not already)
git add Dataset/
git commit -m "Add Dataset files"
git push
```

#### Step 2: Deploy to Render

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Select this repository
6. Render will detect `render.yaml`
7. Click "Create Web Service"

#### Step 3: Wait for First Build

First deployment takes 10-20 minutes because it:
1. Installs Python dependencies
2. Downloads medical PDFs
3. Creates ChromaDB with embeddings

#### Step 4: Get Your URL

Once deployed, you'll get:
```
https://medical-chatbot-api.onrender.com
```

---

## Quick Deploy Commands

```bash
# Make sure you're on main branch
git status

# Add all files
git add .

# Commit
git commit -m "Ready for Render deployment"

# Push to GitHub
git push origin main

# Then go to render.com and connect repo
```

---

## Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Run API
python app.py

# Should start on http://localhost:8001
```

---

## Troubleshooting

### Build Fails
- Check Render logs for errors
- Make sure Dataset files are in repo
- Check Python version compatibility

### Slow First Request
- Normal for ChromaDB initialization
- Subsequent requests are fast

### Memory Errors
- Upgrade Render plan from Free to Starter ($7/month)
- Or reduce dataset size

---

## Expected URL Format

Once deployed:
```
https://medical-chatbot-api.onrender.com
```

API Endpoints:
- `GET /health` - Health check
- `POST /query` - Query endpoint
- `GET /` - Root endpoint

