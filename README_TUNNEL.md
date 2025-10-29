# Bypassing Firewall (Fortinet) to Expose Your API

Your ngrok is blocked by Fortinet. Here are 3 reliable alternatives:

## ✅ Method 1: Cloudflare Tunnel (Recommended)

**Cloudflare Tunnel is the most reliable solution for bypassing Fortinet.**

### Setup:

1. **Cloudflared is already installed!** ✅

2. **Run the tunnel script:**
   ```bash
   ./start_tunnel.sh
   ```

3. **Or manually:**
   ```bash
   # Terminal 1: Start your API (if not running)
   python app.py
   
   # Terminal 2: Start tunnel
   cloudflared tunnel --url http://localhost:8001
   ```

You'll get a URL like: `https://random-word-random-word.trycloudflare.com`

---

## ✅ Method 2: SSH Tunnels (localhost.run or serveo)

**SSH tunnels usually work because port 22 is rarely blocked.**

### Using localhost.run:

```bash
ssh -R 80:localhost:8001 ssh@ssh6.localhost.run
```

You'll get a URL like: `https://random-name.localhost.run`

### Using serveo.net:

```bash
ssh -R 80:localhost:8001 serveo.net
```

---

## ✅ Method 3: Deploy to Production

You already have deployment configs! Deploy to:
- **Render.com** - Recommended
- **Railway.app** 
- **Fly.io**

### Deploy to Render:

1. Push to GitHub
2. Connect to Render
3. Use the provided URL

Your `render.yaml` and other configs are already set up!

---

## Quick Test

Test your exposed URL:
```bash
curl https://YOUR-URL/health
```

Or test the /query endpoint:
```bash
curl -X POST https://YOUR-URL/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are symptoms of heart attack?",
    "top_k": 3
  }'
```

---

## Troubleshooting

### Cloudflare Tunnel shows "Connection refused"
- Make sure `python app.py` is running on port 8001
- Check: `curl http://localhost:8001/health`

### SSH tunnels timeout
- Try a different provider (switch from localhost.run to serveo)
- Check if your firewall blocks SSH on specific ports

### All tunnels fail
- Deploy to Render/Railway (recommended for production)
- Or use a VPN to bypass corporate firewall

---

## Current Status

✅ FastAPI is running on port 8001  
✅ Cloudflared is installed  
✅ Ready to start tunneling!

