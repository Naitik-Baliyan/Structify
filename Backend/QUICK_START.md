# 🚀 Structify Backend - Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Navigate to backend
cd Backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start server
python -m uvicorn main:app --reload
```

✅ Backend running at: `http://127.0.0.1:8000`

---

## Configuration (1 minute)

Edit `.env` file:

```bash
# Default API provider (gemini or openai)
API_PROVIDER=gemini

# Get API key from:
# - Gemini: https://makersuite.google.com/app/apikey
# - OpenAI: https://platform.openai.com/api-keys
GEMINI_API_KEY=your_key_here

# CORS - Frontend origin
FRONTEND_ORIGIN=http://127.0.0.1:3000,http://localhost:3000
```

**Works without API key!** (Uses heuristic analysis)

---

## API Endpoints

### Health Check
```bash
curl http://127.0.0.1:8000/
```

### Analyze Business Idea
```bash
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "AI-powered meal planning app",
    "target_market": "Health-conscious millennials",
    "problem_statement": "People spend too much time planning healthy meals"
  }'
```

**Response:**
```json
{
  "idea": "AI-powered meal planning app",
  "target_market": "Health-conscious millennials",
  "problem_statement": "People spend too much time planning healthy meals",
  "analysis": "Your idea targets...",
  "compatibility_score": 78,
  "improvement_suggestions": [
    "Conduct deeper market research...",
    "Define your total addressable market (TAM)...",
    "Identify early adopter segments..."
  ],
  "risk_level": "medium",
  "domain_tags": ["ai", "saas", "healthcare", "b2c"]
}
```

---

## Project Structure

```
Backend/
├── main.py                # FastAPI app + endpoints
├── requirements.txt       # Dependencies
├── .env                   # Configuration (DO NOT COMMIT)
├── backend.log           # Logs
│
├── BACKEND_SETUP.md               # Full documentation
├── IMPLEMENTATION_SUMMARY.md      # Implementation details
│
└── services/
    ├── __init__.py
    └── ai_engine.py       # AI analysis (550+ lines)
        ├── AIEngine           → generate_analysis_response()
        ├── SuggestionGenerator → generate()
        ├── RiskClassifier     → classify()
        └── DomainTagger       → extract_tags()
```

---

## 🎯 What Each Component Does

### AIEngine
- Calls external AI APIs (Gemini/OpenAI)
- Falls back to heuristics if API fails
- Timeout protection (30s)
- Returns: `{"analysis", "compatibility_score", "improvement_suggestions", "risk_level", "domain_tags"}`

### SuggestionGenerator
- Generates 3-5 startup improvement suggestions
- 4 categories: market, product, business, execution
- Smart selection based on input

### RiskClassifier
- Classifies risk: low, medium, high, critical
- Uses keyword-based heuristic scoring
- Evaluates business viability factors

### DomainTagger
- Extracts industry and domain tags
- 12 categories: tech, fintech, healthcare, saas, etc.
- Multi-tag support (max 6)

---

## 📊 Features

✅ **AI Integration**
- Gemini and OpenAI API support
- Automatic fallback to heuristics
- Async/await for non-blocking calls
- Timeout protection

✅ **Smart Analysis**
- Business idea analysis
- Improvement suggestions
- Risk assessment
- Domain tagging

✅ **Security**
- API keys from environment variables
- CORS restricted to frontend origins
- No hardcoded secrets
- Input validation

✅ **Logging**
- File: `backend.log`
- Console: Real-time monitoring
- Request tracking
- Error tracking

✅ **Backward Compatible**
- No frontend changes needed
- Existing fields still returned
- New fields are enhancements

---

## 🧪 Testing

### Manual Test Script

```python
# test_backend.py
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test health check
print("🏥 Health Check...")
response = requests.get(f"{BASE_URL}/")
print(json.dumps(response.json(), indent=2))

# Test analysis
print("\n📊 Testing Analysis...")
payload = {
    "idea": "AI-powered fitness coach app",
    "target_market": "Busy professionals aged 25-40",
    "problem_statement": "People don't have time for personal trainers but need fitness guidance"
}

response = requests.post(
    f"{BASE_URL}/analyze",
    json=payload,
    headers={"Content-Type": "application/json"}
)

print(json.dumps(response.json(), indent=2))
```

Run:
```bash
pip install requests
python test_backend.py
```

---

## 🔍 Logging & Debugging

**View real-time logs:**
```bash
# Linux/Mac
tail -f Backend/backend.log

# Windows (PowerShell)
Get-Content Backend/backend.log -Wait
```

**Expected log output:**
```
2026-02-21 14:23:45,123 - __main__ - INFO - Health check request received
2026-02-21 14:23:52,789 - __main__ - INFO - Incoming analysis request - Idea: AI fitness...
2026-02-21 14:23:55,234 - __main__ - INFO - Analysis generated successfully - Score: 82
```

**Enable debug mode:**
```python
# In main.py, change:
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

---

## ⚙️ Environment Variables

| Variable | Default | Required |
|----------|---------|----------|
| `API_PROVIDER` | gemini | No |
| `GEMINI_API_KEY` | - | No* |
| `OPENAI_API_KEY` | - | No* |
| `API_TIMEOUT` | 30 | No |
| `FRONTEND_ORIGIN` | localhost:3000 | No |
| `LOG_LEVEL` | INFO | No |

*At least one API key recommended (works without one)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'services'"
```bash
# Make sure you're in Backend directory
cd Backend
python -m uvicorn main:app --reload
```

### "No module named 'google.generativeai'"
```bash
pip install -r requirements.txt
```

### CORS error in frontend console
Check `.env`:
```env
FRONTEND_ORIGIN=http://127.0.0.1:3000,http://localhost:3000
```
Should match your frontend's origin.

### Slow responses
- First request: May be slow (API call)
- If timeout: API provider is slow, heuristics kick in
- Check logs for errors

### API key not recognized
```bash
# Verify .env file
cat .env | grep API_KEY

# Check file exists
ls -la .env
```

---

## 🚀 Deployment

### Local Development
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]
```

Build & Run:
```bash
docker build -t structify-backend .
docker run -p 8000:8000 --env-file .env structify-backend
```

---

## 💡 Code Example: Custom Integration

```python
# In your code
from services import generate_analysis_response

result = generate_analysis_response(
    idea="My startup idea",
    target_market="Enterprise market",
    problem_statement="Solve X problem",
    api_key="your_key",
    api_provider="gemini",
    timeout=30
)

print(result["compatibility_score"])
print(result["improvement_suggestions"])
print(result["risk_level"])
```

---

## 📚 Documentation Files

- **BACKEND_SETUP.md** - Complete setup & configuration guide
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **QUICK_START.md** - This file

---

## 🎯 Common Tasks

### Change API Provider
Edit `.env`:
```env
API_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

### Restrict CORS Further
Edit `.env`:
```env
FRONTEND_ORIGIN=http://localhost:3000
```

### Increase API Timeout
Edit `.env`:
```env
API_TIMEOUT=60
```

### View Analysis Logs
```bash
grep "Analysis generated" Backend/backend.log
```

### Test with Different Inputs
```bash
# Market analysis
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"idea":"Blockchain voting system","target_market":"Global governments","problem_statement":"Secure voting"}'

# Tech startup
curl -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"idea":"No-code AI builder","target_market":"Citizen developers","problem_statement":"Complex AI setup"}'
```

---

## 🔄 Response Format

Every analysis returns:

```json
{
  // Original fields (still here for compatibility)
  "idea": "The idea description",
  "target_market": "Who it's for",
  "problem_statement": "The problem it solves",
  
  // Core analysis
  "analysis": "2-3 paragraph detailed analysis",
  "compatibility_score": 75,  // 0-100, higher is better
  
  // New fields (enhancements)
  "improvement_suggestions": [
    "Suggestion 1",
    "Suggestion 2",
    "Suggestion 3"
  ],
  "risk_level": "medium",  // low, medium, high, critical
  "domain_tags": [
    "saas",
    "b2b",
    "tech"
  ]
}
```

---

## 📞 Help & Support

1. Check `.env` is configured correctly
2. Review `backend.log` for errors
3. Verify `127.0.0.1:8000` is accessible
4. Try health check endpoint first: `GET /`
5. Check CORS origins if frontend fails

---

## ✅ Verification Checklist

- [ ] Dependencies installed: `pip list | grep fastapi`
- [ ] Server running: `GET http://127.0.0.1:8000/`
- [ ] Health check passes: `{"message": "Structify Backend Running"}`
- [ ] Analysis endpoint works: `POST /analyze`
- [ ] Response includes all 8 fields
- [ ] Logs appear in `backend.log`
- [ ] CORS works with frontend
- [ ] No errors in console

---

**Ready to code!** 🚀

Next: Connect frontend to test end-to-end
