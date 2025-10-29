# Deploying to Vercel

## ⚠️ Important Considerations

### Vercel Serverless Limitations

1. **ChromaDB Storage**: ChromaDB files are too large for Vercel's filesystem
2. **Cold Starts**: Serverless functions have cold starts
3. **Timeout**: 10-second timeout on Hobby plan, 60-second on Pro
4. **Size Limits**: Deployment package size limits

## Alternative Solutions

### Option 1: Use ChromaDB Cloud (Recommended)

Sign up for [ChromaDB Cloud](https://www.trychroma.com/) and update your service to use cloud storage instead of local files.

### Option 2: Deploy to Different Platform

Consider these alternatives:
- **Render.com** - Easy deployment with persistent storage ✅
- **Railway.app** - Great for Python APIs
- **Fly.io** - Good Docker support
- **Heroku** - Traditional but works

## If You Must Use Vercel

### Prerequisites

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Create a `.env` file with ChromaDB cloud credentials (if using cloud)

### Deployment Steps

```bash
# Link your project
vercel

# Or deploy
vercel --prod
```

### Configuration

The `vercel.json` has been created with:
- Python runtime
- API routes configured
- CORS enabled

### Challenges You'll Face

1. **ChromaDB Data**: The `chroma_db` directory is too large (~500MB+)
2. **Vector DB**: Need persistent storage or cloud DB
3. **Cold Starts**: First request will be slow

## Recommended: Deploy to Render

Your project already has `render.yaml` configured!

```bash
# Just push to GitHub and connect to Render
git add .
git commit -m "Ready for deployment"
git push origin main

# Then connect to Render:
# 1. Go to render.com
# 2. Connect your GitHub repo
# 3. Use the render.yaml config
# 4. Deploy!
```

Render provides:
- ✅ Persistent storage for ChromaDB
- ✅ No cold starts
- ✅ Auto-scaling
- ✅ Free tier available

## Summary

**For this project, I recommend deploying to Render or Railway instead of Vercel because:**
- ChromaDB needs persistent storage
- Large database files (10,922 documents)
- Better suited for container-based deployment

Would you like me to help you deploy to Render instead?

