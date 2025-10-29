# 🏥 Medical Chatbot - Access Your Services

## ✅ All Services Running!

### Your URLs:

#### 🌐 Frontend (Main Interface)
```
http://localhost:8080
```
**Open this in your browser to use the chatbot!**

#### 📡 API Server
```
http://localhost:8001
```
Health check: http://localhost:8001/health

---

## Quick Test

### 1. Test Frontend
Open in browser: **http://localhost:8080**

### 2. Test API
```bash
# Health check
curl http://localhost:8001/health

# Test query
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a heart attack?", "top_k": 3}'
```

---

## If You See "Site Can't Be Reached"

### Check 1: Is the frontend running?
```bash
curl http://localhost:8080/
```
Should show HTML. If not, start it:
```bash
cd /Users/thrishithreddy/Desktop/HAC
python3 frontend_server.py &
```

### Check 2: Is the API running?
```bash
curl http://localhost:8001/health
```
Should return: `{"status":"healthy"}`

If not, start it:
```bash
cd /Users/thrishithreddy/Desktop/HAC
python3 app.py &
```

### Check 3: Restart everything
```bash
cd /Users/thrishithreddy/Desktop/HAC
./start_all.sh
```

---

## Current Status

- ✅ Frontend: Running on port 8080
- ✅ API: Running on port 8001  
- ✅ ChromaDB: 10,922 documents indexed
- ✅ Single source: Answers from ONE reliable source
- ✅ No sources: Contexts not shown in chatbox

---

## Use It Now!

1. **Open browser**: http://localhost:8080
2. **Ask questions** about medical topics
3. **Get single, precise answers** from ChromaDB

Example questions:
- "What is a heart attack?"
- "How does insulin work?"
- "What causes diabetes?"

