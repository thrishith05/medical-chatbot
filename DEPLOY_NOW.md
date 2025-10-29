# 🚀 DEPLOY TO RENDER NOW

## Your Project is Ready!

Everything is configured for Render deployment.

### ✅ Files Ready:
- `render.yaml` - Deployment config
- `requirements.txt` - Dependencies
- `Procfile` - Start command
- `runtime.txt` - Python version
- `app.py` - API server

---

## 🚀 3 Simple Steps to Deploy:

### Step 1: Push to GitHub
```bash
git commit -m "Ready for Render deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to **https://render.com**
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select this repository: **HAC**
5. Render will auto-detect `render.yaml`
6. Click **"Create Web Service"**

### Step 3: Wait & Get URL
- First build: 15-20 minutes
- You'll get: `https://medical-chatbot-api.onrender.com`

---

## 📍 Your Deployment URL Will Be:

```
https://medical-chatbot-api.onrender.com
```

### API Endpoints:
- Health: `GET https://medical-chatbot-api.onrender.com/health`
- Query: `POST https://medical-chatbot-api.onrender.com/query`

### Test After Deploy:
```bash
# Test health
curl https://medical-chatbot-api.onrender.com/health

# Test query
curl -X POST https://medical-chatbot-api.onrender.com/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a heart attack?", "top_k": 3}'
```

---

## ⚠️ Important Notes:

1. **First build takes 15-20 minutes** (ChromaDB initialization)
2. **Free tier may sleep after 15min** - Upgrade to Starter ($7/mo) for always-on
3. **Cold starts** - First request after sleep takes ~30 seconds

---

## 🎯 Next Steps:

```bash
# 1. Commit (if not done)
git add .
git commit -m "Ready for Render"
git push

# 2. Go to render.com and deploy
# 3. Get your URL
# 4. Test the API
```

---

## ✅ What You Get:

- ✅ **Live API URL** from Render
- ✅ **Persistent ChromaDB** storage
- ✅ **Auto-scaling** with Render
- ✅ **Production-ready** deployment

**Your API will be live at: https://medical-chatbot-api.onrender.com**

