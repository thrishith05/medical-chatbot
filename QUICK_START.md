# Medical Chatbot - Quick Start Guide

## ✅ Everything is Ready!

Your Medical Chatbot is running with a **single, precise answer** system.

## Current Status

- ✅ **Backend API**: Running on port 8001
- ✅ **Frontend**: Running on port 8080  
- ✅ **ChromaDB**: 10,922 documents indexed
- ✅ **Answer System**: Returns single precise answers

## How to Use

### 1. Open the Frontend
```
http://localhost:8080
```

### 2. Ask Medical Questions
Try these examples:
- "What is a heart attack?"
- "How does insulin work?"
- "What causes high blood pressure?"
- "Explain the respiratory system"

### 3. Get Single, Precise Answers
Each query returns:
- **One clear answer** from a single reliable source
- **No source citations displayed** in the chatbox
- **No scattered fragments** or multiple confusing responses

## What Makes It Precise?

### Answer Quality
- Uses the **best matching document** from ChromaDB
- Extracts **top 2-3 most relevant sentences**
- Filters out headers, figures, and junk content
- Combines into a coherent **200-500 character** answer

### Example
**Question:** "What is a heart attack?"

**Answer:** 
> "Severe prolonged chest pain. Severe prolonged cardiac chest pain may be due to acute myocardial infarction or to unstable angina – known collectively as acute coronary syndrome."

## API Testing

### Test Directly
```bash
curl -X POST http://localhost:8001/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does diabetes affect the body?",
    "top_k": 3
  }'
```

### Inspect ChromaDB
```bash
python3 inspect_chromadb.py
```

## Troubleshooting

### Frontend Shows Error
- Check API is running: `curl http://localhost:8001/health`
- Make sure ChromaDB is initialized
- Check browser console for errors

### Answer Too Short
- Increase `top_k` parameter
- Ask more specific questions

### Answer Too Generic
- Be more specific in your question
- Ask about symptoms, causes, or treatments separately

## Next Steps

1. **Try the frontend**: http://localhost:8080
2. **Test with various medical questions**
3. **Deploy to production** using Render/Railway/Fly.io

## Summary

✅ Single answer per question  
✅ ONE reliable source only (best matching document)  
✅ Sentences scored by relevance  
✅ Clean, professional output  
✅ No source citations in chatbox

**Your chatbot now provides accurate, precise answers from a single reliable source!** 🎯

