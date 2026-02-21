# Structify Backend Setup & Implementation Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Install Dependencies**
```bash
cd Backend
pip install -r requirements.txt
```

2. **Configure Environment Variables**
Edit `.env` file with your API credentials:
```bash
# API Configuration
API_PROVIDER=gemini  # or openai
GEMINI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# CORS Configuration
FRONTEND_ORIGIN=http://localhost:3000,http://127.0.0.1:3000
```

3. **Run Backend Server**
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Server runs at: `http://127.0.0.1:8000`

---

## 📁 Project Structure

```
Backend/
├── main.py                 # FastAPI application & endpoints
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration (DO NOT COMMIT)
├── backend.log            # Logging output
│
└── services/              # Business logic modules
    ├── __init__.py        # Package exports
    └── ai_engine.py       # AI processing & analysis
        ├── AIEngine          # Main service class
        ├── SuggestionGenerator    # Improvement suggestions
        ├── RiskClassifier        # Risk assessment
        └── DomainTagger          # Industry tagging
```

---

## 🔧 Implementation Details

### Step 1: Environment Configuration

**File:** `.env`

The application loads API keys securely using `python-dotenv`:
- Supports both Gemini and OpenAI APIs
- Graceful fallback to heuristic analysis if no key provided
- CORS origins configurable for security

```python
# In main.py - Environment loading
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
```

### Step 2: AI Processing Service Layer

**File:** `services/ai_engine.py`

#### `AIEngine` Class
Main service for analysis generation with async support.

**Key Method:**
```python
async def generate_analysis_response(
    idea: str,
    target_market: str,
    problem_statement: str
) -> Dict
```

Returns:
```json
{
  "analysis": "Detailed business analysis text...",
  "compatibility_score": 75,
  "improvement_suggestions": ["suggestion 1", "suggestion 2", ...],
  "risk_level": "medium",
  "domain_tags": ["tech", "b2b"]
}
```

**Features:**
- ✅ Async/await support for non-blocking API calls
- ✅ Timeout protection (30s default, configurable)
- ✅ Error handling with heuristic fallback
- ✅ Structured JSON response format

### Step 3: Suggestion Generator

**Class:** `SuggestionGenerator`

Generates 3-5 contextual improvement suggestions:
- Market research recommendations
- Product development strategies
- Business model guidance
- Execution planning

```python
suggestions = SuggestionGenerator.generate(idea, target_market, problem_statement)
# Returns: ["Conduct market research...", "Define your TAM...", ...]
```

### Step 4: Risk Classification

**Class:** `RiskClassifier`

Rule-based risk assessment:
- **Risk Levels:** low, medium, high, critical
- **Keyword Analysis:** Positive/negative indicators
- **Heuristic Scoring:** Accumulates risk score

```python
risk = RiskClassifier.classify(idea, target_market, problem_statement)
# Returns: "medium"
```

### Step 5: Domain Tagging

**Class:** `DomainTagger`

Keyword-based industry and domain extraction:
- tech, fintech, healthcare, ecommerce
- education, social, logistics, energy
- environment, entertainment, b2b, b2c

```python
tags = DomainTagger.extract_tags(idea, target_market, problem_statement)
# Returns: ["saas", "b2b", "tech"]
```

### Step 6: Logging System

**Configuration:** Dual channel logging

1. **File Logging** → `backend.log`
2. **Console Logging** → Terminal output

**Log Format:**
```
2026-02-21 10:30:45,123 - __main__ - INFO - Incoming analysis request - Idea: AI-powered...
```

**Logged Events:**
- ✅ Incoming analysis requests
- ✅ API responses & scores
- ✅ Errors with full traceback
- ✅ Health check requests
- ⚠️ Validation failures
- ℹ️ API fallback notifications

### Step 7: Timeout Protection

**Implementation:**
```python
# Gemini API
response = await asyncio.wait_for(
    asyncio.to_thread(model.generate_content, prompt),
    timeout=self.timeout  # Default: 30 seconds
)

# OpenAI API
async with asyncio.timeout(self.timeout):
    # Request code here
```

**Configuration:**
```env
API_TIMEOUT=30  # seconds
```

---

## 📡 API Endpoints

### Health Check
```
GET /
Response: {"message": "Structify Backend Running 🚀", "timestamp": "2026-02-21T..."}
```

### Business Idea Analysis
```
POST /analyze
Content-Type: application/json

Request:
{
  "idea": "AI-powered meal planning app",
  "target_market": "Health-conscious millennials",
  "problem_statement": "People spend too much time planning healthy meals"
}

Response:
{
  "idea": "AI-powered meal planning app",
  "target_market": "Health-conscious millennials",
  "problem_statement": "People spend too much time planning healthy meals",
  "analysis": "Your idea...",
  "compatibility_score": 78,
  "improvement_suggestions": [
    "Conduct deeper market research...",
    "Define your TAM...",
    ...
  ],
  "risk_level": "medium",
  "domain_tags": ["ai", "saas", "healthcare", "b2c"]
}
```

---

## 🔒 Security Features

### 1. API Key Management
```python
# Secure random location (not in version control)
api_key = os.getenv("GEMINI_API_KEY")
```

### 2. CORS Restrictions
```python
# Only allow specified frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"]
)
```

### 3. Input Validation
```python
# Whitespace validation
if not data.idea.strip() or not data.target_market.strip():
    raise HTTPException(status_code=400, detail="...")
```

### 4. Environment Isolation
- `.env` file excluded from version control (.gitignore)
- No hardcoded secrets in source code
- Graceful degradation without API key

---

## 🎯 MVP Heuristic Analysis

When external AI APIs are unavailable:

### Compatibility Score Calculation
- Base score: 60/100
- +3 points per positive keyword (innovative, scalable, etc.)
- -5 points per negative keyword (unclear, vague, etc.)
- Clamped: 20-100 range

### Risk Classification Algorithm
```
if risk_score >= 5 → "high"
elif risk_score >= 2 → "medium"
else → "low"
```

---

## 🧪 Testing & Validation

### Manual Testing
```bash
# Terminal 1: Start backend
python -m uvicorn main:app --reload

# Terminal 2: Test health check
curl http://localhost:8000/

# Terminal 3: Test analysis
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"idea":"My idea","target_market":"Everyone","problem_statement":"A problem"}'
```

### Frontend Compatibility
✅ **Backward Compatible:** No changes required to frontend
- Existing fields still returned in same format
- Additional fields are bonus enhancements
- Graceful degradation if new fields missing

---

## 📋 Configuration Reference

### Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `API_PROVIDER` | No | gemini | API service selection |
| `GEMINI_API_KEY` | No | - | Google Gemini credentials |
| `OPENAI_API_KEY` | No | - | OpenAI API credentials |
| `API_TIMEOUT` | No | 30 | Request timeout (seconds) |
| `FRONTEND_ORIGIN` | No | localhost:3000,127.0.0.1:3000 | CORS allowed origins |
| `LOG_LEVEL` | No | INFO | Logging verbosity |
| `ENABLE_HEURISTIC_FALLBACK` | No | true | Use fallback when API fails |

---

## 🚨 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'services'"
```bash
# Ensure you're running from Backend directory
cd Backend
python -m uvicorn main:app --reload
```

### Issue: "API key not found" (using heuristics)
```bash
# Check .env file exists and has API_KEY set
cat .env | grep API_KEY
```

### Issue: CORS errors in frontend
```env
# Verify FRONTEND_ORIGIN matches frontend's origin
FRONTEND_ORIGIN=http://127.0.0.1:5500,http://localhost:3000
```

### Issue: Slow analysis response
- Check network connectivity to external AI API
- Increase `API_TIMEOUT` in .env if needed
- Review `backend.log` for error details

---

## 📊 Logging Output Example

```
2026-02-21 14:23:45,123 - __main__ - INFO - CORS Origins configured: ['http://127.0.0.1:3000']
2026-02-21 14:23:50,456 - __main__ - INFO - Health check request received
2026-02-21 14:23:52,789 - __main__ - INFO - Incoming analysis request - Idea: AI healthcare...
2026-02-21 14:23:53,012 - services.ai_engine - INFO - AIEngine initialized with provider: gemini
2026-02-21 14:23:55,234 - services.ai_engine - INFO - Analysis generated successfully - Score: 82
2026-02-21 14:23:55,456 - __main__ - INFO - Analysis generated successfully - Score: 82
```

---

## 🎓 Architecture Overview

```
┌─────────────────────────────────────────┐
│         Frontend (JavaScript)           │
│  (chat.js sends POST /analyze)          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│     FastAPI Application (main.py)       │
│  ├─ CORS Middleware (Security)          │
│  ├─ Request Validation                   │
│  ├─ Environment Configuration            │
│  └─ /analyze Endpoint                    │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│    AI Engine Service (ai_engine.py)    │
│  ├─ Try External API (Gemini/OpenAI)   │
│  └─ Fallback: Heuristic Analysis       │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┬─────────┐
        ▼          ▼          ▼         ▼
   [Suggestions] [Risk] [Domain]  [Score]
                   │
                   ▼
        Response JSON Structure
        {"analysis", "score", ...}
```

---

## 🔄 Future Enhancement Ideas

1. **Database Integration** - Store analysis history
2. **User Authentication** - Track user requests
3. **Advanced ML Models** - Replace heuristics with trained models
4. **Rate Limiting** - Prevent API abuse
5. **Caching** - Cache similar analysis requests
6. **Async Task Queue** - Handle long-running analysis (Celery)
7. **A/B Testing** - Compare response formats
8. **Analytics** - Track which suggestions are most helpful

---

## 📞 Support

For issues or questions:
1. Check `backend.log` for error details
2. Review this documentation
3. Test endpoints with provided curl commands
4. Check GitHub issues or project documentation

---

## 📄 Files Modified/Created

**Created:**
- ✅ `Backend/.env` - Environment configuration
- ✅ `Backend/requirements.txt` - Dependencies
- ✅ `Backend/services/__init__.py` - Package module
- ✅ `Backend/services/ai_engine.py` - Core AI engine (550+ lines)

**Modified:**
- ✅ `Backend/main.py` - Enhanced with logging, AI integration, extended response model

**Unchanged:**
- ✅ `Frontend/chat.js` - No changes required
- ✅ `Frontend/config.js` - Compatible with new response format
- ✅ All HTML and CSS files

---

**Version:** 1.0.0  
**Last Updated:** February 21, 2026  
**Status:** MVP Ready for Hackathon Demo 🚀
