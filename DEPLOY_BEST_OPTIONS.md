# 🚀 Best Deployment Options

## Top Recommendations (in order)

### 1. **Render.com** ⭐ RECOMMENDED
**Best for:** Easy setup, persistent storage included

**Why it's best:**
- ✅ Free tier available
- ✅ Persistent disk storage (keeps chroma_db)
- ✅ Auto-deploy from GitHub
- ✅ Environment variables support
- ✅ Already have render.yaml configured

**Deployment steps:**
1. Push code to GitHub
2. Connect GitHub to Render
3. Select this repository
4. Add environment variable: `PYTHON_VERSION=3.9`
5. Click "Deploy"
6. Wait 10 minutes for build

**URL:** https://your-app-name.onrender.com

---

### 2. **Railway.app** ⭐ ALTERNATIVE
**Best for:** Fastest deployment, Docker support

**Why it's good:**
- ✅ Simpler than Render
- ✅ Better free tier
- ✅ One-click deploy from GitHub
- ⚠️ Need to handle chroma_db persistence

---

### 3. **Fly.io**
**Best for:** Global edge deployment

**Why it's good:**
- ✅ Edge computing
- ✅ Persistent volumes
- ⚠️ More complex setup

---

## ⚠️ CRITICAL: Pre-build chroma_db

**You MUST upload the chroma_db folder!**

Your local chroma_db (112MB) took ~25 minutes to build. 
Deploying without it would require rebuilding on first request (too slow).

### Option A: Upload chroma_db via Git (Easiest)

```bash
cd /Users/thrishithreddy/Desktop/HAC
git init
git add .
git commit -m "Initial commit"
# Create a new repo on GitHub and push
```

**Pros:** Automatic, versioned
**Cons:** 112MB in repo (slightly slow to clone)

### Option B: Upload chroma_db separately (Better)

1. Upload chroma_db to cloud storage
2. Download on first deploy
3. Use it from there

---

## 📋 Pre-Deployment Checklist

- [x] chroma_db created locally (112MB)
- [x] API tested locally (all endpoints working)
- [ ] Code pushed to GitHub
- [ ] Environment variables configured
- [ ] Documentation updated

---

## 🎯 Quick Deploy - Render.com (RECOMMENDED)

**Time:** 15 minutes total

### Step 1: Push to GitHub (5 min)
```bash
cd /Users/thrishithreddy/Desktop/HAC
git init
git add .
git commit -m "Medical chatbot API"
# Push to GitHub (create repo first)
```

### Step 2: Deploy on Render (5 min)
1. Go to render.com
2. Sign up (free)
3. "New Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Step 3: Wait for deployment (5 min)
- Render installs dependencies
- API starts
- Your API is live!

**Your URL:** `https://medical-chatbot-xyz.onrender.com`

---

## 🔧 Configuration Needed

Update `app.py` to use environment port:
```python
import os
port = int(os.environ.get("PORT", 8001))
uvicorn.run(app, host="0.0.0.0", port=port)
```

---

## ✅ Post-Deployment

Test your deployed API:
```bash
curl https://your-app.onrender.com/health
curl -X POST https://your-app.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is hypertension?","top_k": 2}'
```

---

## 💡 Adding the 9th PDF Later

After deployment:
1. SSH into server (or use Render shell)
2. Edit `services/rag_service.py` line 130: `[:8]` → `[:9]`
3. Restart the service
4. Only the 9th PDF gets processed (fast!)

