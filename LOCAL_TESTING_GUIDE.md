# 🔧 Local Testing - Quick Guide

## ✅ Status: Everything is Fixed!

The backend and frontend are now properly configured and communicating.

### What Was Wrong
1. **Auth Check** - Chat was redirecting to login.html before showing the interface
2. **Backend URL Fallback** - getBackendUrl() was defaulting to port 8000 instead of 8001
3. **Error Messages** - Error messages weren't informative enough

### What Was Fixed
1. ✅ Auth check now allows dev access (no login required)
2. ✅ Backend URL now correctly defaults to 8001
3. ✅ Added detailed logging to browser console
4. ✅ Improved error messages show backend URL

---

## 🚀 How to Run Locally

### Option 1: One-Click Startup (EASIEST)
```batch
Double-click: C:\Users\ASUS\Desktop\Structify\START.bat
```
This will:
- Start both backend and frontend in separate windows
- Open browser automatically
- Keep both servers running

### Option 2: Manual Startup
**Terminal 1 - Backend**:
```bash
cd c:\Users\ASUS\Desktop\Structify\Backend
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```
Keep this window open!

**Terminal 2 - Frontend**:
```bash
cd c:\Users\ASUS\Desktop\Structify\Frontend
python -m http.server 5500
```
Keep this window open!

**Browser**:
```
http://localhost:5500/chat.html
```

---

## 🐛 Debugging

### Check Browser Console (F12)
1. Press **F12** to open Developer Tools
2. Click **Console** tab
3. Look for:
   - `[chat.js] Backend URL: http://127.0.0.1:8001` ← Should see this
   - `[analyzeWithBackend] Calling: http://127.0.0.1:8001/analyze` ← Should see when submitting
   - Any red error messages ← These indicate problems

### If You See Errors
1. **Connection refused** → Backend not running
   - Fix: Start backend on port 8001
   
2. **CORS error** → Origin not allowed
   - Fix: Check `Backend/main.py` line 33 includes `http://localhost:5500`
   - Current allowed origins: localhost:3000, 127.0.0.1:3000, localhost:5500, 127.0.0.1:5500

3. **Backend connection failed** → Check error message
   - Shows the actual backend URL being used
   - Shows the error details

### Run Diagnostic Tests
```bash
cd Backend
python cors_test.py       # Tests CORS and connectivity
python quick_diagnostic.py # Quick health check
python test_api.py all    # Full test suite
```

---

## 📋 Testing Checklist

- [ ] Backend running on http://127.0.0.1:8001
- [ ] Frontend running on http://localhost:5500
- [ ] Browser opens to http://localhost:5500/chat.html
- [ ] Chat welcome message appears
- [ ] No red errors in browser console (F12)
- [ ] Can type in the chat box
- [ ] After 3 messages, analysis appears
- [ ] "📄 Generate BRD" button appears in analysis
- [ ] Can click button to open format selector

---

## 🎯 Complete Test Flow

1. **Open Chat**
   ```
   http://localhost:5500/chat.html
   ```

2. **Message 1** - Enter your business idea
   ```
   "AI-powered fitness coaching app"
   ```

3. **Message 2** - Enter target market
   ```
   "Busy professionals aged 25-40"
   ```

4. **Message 3** - Enter problem statement
   ```
   "People need fitness guidance but can't afford personal trainers"
   ```

5. **Expect**: Analysis with score, suggestions, risk level, and "Generate BRD" button

6. **Click**: "📄 Generate BRD"

7. **Select**: Format (PDF recommended)

8. **Click**: "Generate Document"

9. **Result**: File downloads (BRD_[idea_name].pdf)

---

## 🔗 Important URLs

| Service | URL | Port |
|---------|-----|------|
| **Backend API** | http://127.0.0.1:8001 | 8001 |
| **Frontend** | http://localhost:5500 | 5500 |
| **Chat Page** | http://localhost:5500/chat.html | 5500 |
| **Config File** | Frontend/config.js | N/A |

---

## 📝 Configuration Files

### Backend/.env
```env
API_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyDI-qpisXmOzAmD_iWasc4J38SsEDoYmGc
FRONTEND_ORIGIN=http://localhost:3000,...,http://localhost:5500,http://127.0.0.1:5500
API_TIMEOUT=30
```

### Frontend/config.js
```javascript
const API_CONFIG = {
  BACKEND_URL: 'http://127.0.0.1:8001',
  TIMEOUT: 10000,
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000
};
```

---

## 🆘 Still Having Issues?

1. **Close everything** - Close all VS Code terminals, Chrome, everything
2. **Check ports**:
   ```powershell
   netstat -ano | findstr "8001\|5500"
   ```
   If ports are in use, kill the processes:
   ```powershell
   taskkill /F /PID [PID_NUMBER]
   ```
3. **Start fresh** - Use START.bat to launch everything
4. **Check console** - Press F12 in browser, look for error messages
5. **Run diagnostic** - `python Backend/cors_test.py`

---

## ✨ What's Working Now

✅ Backend API serving on port 8001  
✅ Frontend UI serving on port 5500  
✅ CORS headers properly configured  
✅ Chat interface loads without auth redirect  
✅ Backend logging shows all requests  
✅ Error messages show actual backend URL  
✅ BRD generation all 4 formats working  
✅ File downloads working  

---

**Go ahead and test it! Everything should work now.** 🎉
