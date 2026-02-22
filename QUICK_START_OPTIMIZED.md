# Quick Start: Optimized Structify Demo

**Last Updated:** February 21, 2026  
**Status:** ✅ Ready to Run

---

## System Requirements

- Python 3.8+
- Windows/Mac/Linux
- Modern browser (Chrome, Firefox, Edge, Safari)
- Port 8000 (Backend) and 5500 (Frontend) available

---

## Quick Start (3 Steps)

### Step 1: Start Backend Server

Open **PowerShell or Terminal** and run:

```powershell
cd c:\Users\ASUS\Desktop\Structify\Backend
pip install -r requirements.txt  # First time only
python -m uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     CORS configured: All origins allowed for prototype demo
```

✅ Backend is running and ready for API calls.

---

### Step 2: Start Frontend Server

Open a **New PowerShell or Terminal** and run:

```powershell
cd c:\Users\ASUS\Desktop\Structify\Frontend
python -m http.server 5500
```

**Expected Output:**
```
Serving HTTP on 127.0.0.1 port 5500 (http://127.0.0.1:5500/)
```

✅ Frontend is ready to serve HTML/CSS/JS.

---

### Step 3: Open in Browser

Click or navigate to:

```
http://localhost:5500/chat.html
```

Or use the alternative URL:

```
http://127.0.0.1:5500/chat.html
```

✅ Chat interface is now live!

---

## Demo Workflow

1. **Enter Your Business Idea**
   - Example: "An AI-powered customer service chatbot"
   - Click "Send" or press Enter

2. **Describe Your Target Market**
   - Example: "Mid-market SaaS companies"
   - Click "Send"

3. **State the Problem Your Idea Solves**
   - Example: "Reduce support team workload"
   - Click "Send"

4. **View Analysis Results**
   - Backend analyzes your idea
   - Shows compatibility score, risk level, domain tags
   - Displays improvement suggestions

5. **Generate BRD Document** (Optional)
   - Click "📄 Generate BRD" button
   - Select format: PDF, DOCX, TXT, or Image
   - Click "Generate"
   - File downloads to your computer

---

## API Endpoints

### Health Check
```
GET http://127.0.0.1:8000/
Returns: { "message": "Structify Backend Running 🚀", "timestamp": "..." }
```

### Analyze Business Idea
```
POST http://127.0.0.1:8000/analyze
Body: {
  "idea": "Your business idea",
  "target_market": "Description of target market",
  "problem_statement": "Problem your idea solves"
}

Response: {
  "idea": "...",
  "target_market": "...",
  "problem_statement": "...",
  "analysis": "...",
  "compatibility_score": 75,
  "improvement_suggestions": ["...", "..."],
  "risk_level": "medium",
  "domain_tags": ["tech", "saas"]
}
```

### Generate BRD
```
POST http://127.0.0.1:8000/generate_brd
Body: {
  "format": "pdf|docx|txt|image",
  "analysis_data": { ... }  // From /analyze response
}

Response: Binary file (downloads as BRD_[idea_name].[format])
```

---

## Troubleshooting

### ❌ "Backend unreachable" Error

**Solution:**
1. Verify backend is running: Check Step 1 output
2. Kill any process on port 8000:
   ```powershell
   Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | ForEach-Object { taskkill /F /PID $_.OwningProcess }
   ```
3. Restart backend: `python -m uvicorn main:app --reload`

### ❌ "Port 5500 already in use" Error

**Solution:**
```powershell
# Kill process on port 5500
Get-NetTCPConnection -LocalPort 5500 -ErrorAction SilentlyContinue | ForEach-Object { taskkill /F /PID $_.OwningProcess }

# Start frontend on different port
python -m http.server 5501
# Then access: http://localhost:5501/chat.html
```

### ❌ "JSON parsing error" or Invalid Response

**Possible Causes:**
- Gemini/OpenAI API key not set in `.env`
- API quota exhausted
- Network connectivity issue

**Solution:**
1. Check `.env` file has `GEMINI_API_KEY` or `OPENAI_API_KEY`
2. Check browser console (F12) for detailed error
3. Review backend logs (terminal where uvicorn is running)
4. Try fallback heuristic mode (auto-enabled if no API key)

### ❌ BRD Download Fails

**Solution:**
1. Ensure backend is still running
2. Clear browser cache (Ctrl+Shift+Delete)
3. Check file permissions in Backend folder
4. Review browser console for errors
5. Try a different file format

---

## Configuration

### Backend Settings

Edit `.env` file in Backend folder:

```env
# API Configuration
GEMINI_API_KEY=your_key_here
# OR
OPENAI_API_KEY=your_key_here

# Settings
API_PROVIDER=gemini
API_TIMEOUT=30
```

### Frontend Settings

Edit `config.js` in Frontend folder:

```javascript
const API_CONFIG = {
  BACKEND_URL: 'http://127.0.0.1:8000',  // Change if backend is on different machine
  TIMEOUT: 10000,          // Request timeout in ms
  RETRY_ATTEMPTS: 2,       // Auto-retry count
  RETRY_DELAY: 500         // Initial retry delay in ms
};
```

---

## Development Tips

### Auto-reload Backend
Backend automatically reloads on file changes (--reload flag active):
- Modify `services/ai_engine.py`
- Server restarts automatically
- No need to restart manually

### Debug Frontend
Open **Developer Tools** (F12):
1. **Console Tab:** View error messages
2. **Network Tab:** Monitor API calls
3. **Application Tab:** Check localStorage data

View detailed logs like:
```
[chat.js] Backend URL: http://127.0.0.1:8000
[analyzeWithBackend] Calling: http://127.0.0.1:8000/analyze
[fetchWithRetry] Attempt 1/2 failed with status 500. Retrying in 500ms...
```

### Test API Directly

Using PowerShell:
```powershell
$body = @{
  idea = "AI chatbot"
  target_market = "SaaS"
  problem_statement = "Support costs"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8000/analyze" `
  -Method Post `
  -Headers @{"Content-Type" = "application/json"} `
  -Body $body
```

---

## Performance Notes

### Optimizations Made

✅ **Reduced Retry Attempts:** 3 → 2 (faster feedback)  
✅ **Optimized Retry Delay:** 1000ms → 500ms base  
✅ **DOM Rendering:** Uses requestAnimationFrame (no jank)  
✅ **Error Handling:** Robust with specific messages  
✅ **Request Timeout:** 10 seconds (appropriate for AI calls)  

### Expected Performance Times

- **Analysis Request:** 2-10 seconds (depends on Gemini/OpenAI API)
- **Fallback Heuristic:** <1 second
- **BRD Generation:** 5-15 seconds (PDF/DOCX) or 10-30s (Images)
- **Network Retry:** Automatic, ~500-1000ms between attempts

---

## Security Notes

⚠️ **Important for Production:**

Current setup is for **Demo/Prototype** only:
- CORS allows all origins (`"*"`)
- No authentication on backend API
- Suitable for localhost testing

**For Production:**
1. Restrict CORS origins
2. Add API key authentication
3. Implement rate limiting
4. Use HTTPS
5. Add request validation
6. Implement audit logging

---

## File Structure

```
Structify/
├── Backend/
│   ├── main.py              # FastAPI app (port 8000)
│   ├── services/
│   │   ├── ai_engine.py     # AI processing
│   │   ├── brd_generator.py # Document generation
│   ├── requirements.txt
│   └── .env                 # API keys (not in repo)
│
├── Frontend/
│   ├── config.js            # API configuration (port 8000)
│   ├── chat.js              # Chat logic
│   ├── chat.html            # Main UI
│   ├── auth.js              # Authentication
│   ├── style.css            # Styling
│
└── RUNTIME_OPTIMIZATION_SUMMARY.md  # This optimization document
```

---

## Support

### Check Application Status

1. **Backend Healthy?**
   ```bash
   curl http://127.0.0.1:8000/
   ```
   Should return: `{"message": "Structify Backend Running 🚀", ...}`

2. **Frontend Loaded?**
   - Open `http://localhost:5500/chat.html`
   - Should see chat interface
   - Check browser console (F12) for errors

3. **API Connection Working?**
   - Type your idea in chat
   - Should trigger request visible in Network tab (F12)
   - Check backend terminal for log output

### Debug Checklist

- [ ] Backend running on 8000 (`uvicorn main:app --reload`)
- [ ] Frontend running on 5500 (`python -m http.server 5500`)
- [ ] Browser opened to `http://localhost:5500/chat.html`
- [ ] Viewing correct URL (not accessing from file://)
- [ ] No ports blocked by firewall
- [ ] API key set in `.env` if using external APIs
- [ ] Browser console shows no errors (F12)
- [ ] Network tab shows requests going to correct URL (F12)

---

## Next Steps

1. ✅ Run the demo
2. ✅ Test with your business ideas
3. ✅ Try generating BRDs in different formats
4. ✅ Explore the code and customize as needed
5. ✅ Refer to [RUNTIME_OPTIMIZATION_SUMMARY.md](RUNTIME_OPTIMIZATION_SUMMARY.md) for technical details

---

**Ready to go!** Start with Step 1 above. 🚀
