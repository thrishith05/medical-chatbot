# Medical Chatbot Frontend

A modern, responsive frontend for the Medical Chatbot API.

## Features

- 🎨 **Modern UI**: Clean, professional design with gradient background
- 💬 **Chat Interface**: Real-time chat experience
- 📚 **Citation Display**: Shows source contexts for every answer
- 📱 **Responsive**: Works on desktop and mobile devices
- ⚡ **Fast**: No framework overhead, pure HTML/CSS/JavaScript
- 🔄 **Auto-connect**: Checks API health automatically

## Quick Start

### Option 1: Using Python Server (Recommended)

```bash
# From project root
python frontend_server.py
```

This will:
- Start server on http://localhost:8080
- Open browser automatically
- Serve the frontend files

### Option 2: Using SimpleHTTPServer

```bash
cd frontend
python -m http.server 8080
```

Then open: http://localhost:8080

### Option 3: Using VS Code Live Server

Right-click on `index.html` → "Open with Live Server"

## Configuration

The frontend automatically connects to the API URL configured in the input field at the bottom of the page.

Default API URL: `http://localhost:8001`

You can change it to:
- Your tunnel URL: `https://random-words.trycloudflare.com`
- Your production URL: `https://your-app.onrender.com`
- Any custom API endpoint

## Usage

1. **Start Backend**: Make sure your FastAPI app is running
   ```bash
   python app.py
   ```

2. **Start Frontend**: Run the frontend server
   ```bash
   python frontend_server.py
   ```

3. **Ask Questions**: Type your medical question and click Send

4. **View Sources**: Each answer includes source contexts from medical documents

## Example Questions

- "What are the symptoms of a heart attack?"
- "How does aspirin work?"
- "What causes diabetes?"
- "Explain the digestive process"
- "What are the types of blood cells?"

## Components

- `index.html`: Main HTML structure
- `style.css`: Modern CSS styling with gradients and animations
- `app.js`: API integration and UI logic

## API Compatibility

The frontend expects the backend to have:
- `POST /query` - Submit medical queries
- `GET /health` - Health check endpoint
- CORS enabled (already configured in your backend)

## Troubleshooting

### "Connection Error"
- Check if the API URL is correct
- Ensure the backend is running on the specified port
- Check browser console for detailed errors

### CORS Errors
- Your backend already has CORS configured
- If issues persist, check the browser console

### Port Already in Use
- Change the port in `frontend_server.py`
- Or use a different port: `python -m http.server 9000`

## Deployment

To deploy the frontend:

1. **Static Hosting**: Upload `frontend/` folder to:
   - Netlify
   - Vercel
   - GitHub Pages
   - AWS S3

2. **Update API URL**: Make sure to update the default API URL to your production backend

3. **HTTPS**: Ensure your backend API supports HTTPS for secure connections

