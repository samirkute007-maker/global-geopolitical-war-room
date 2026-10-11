# GLOBAL GEOPOLITICAL WAR ROOM

> **Geopolitics → Economy → Markets → Assets**  
> AI & Mock Intelligence Macro-Financial War Room Dashboard.

---

## 🏛️ Project Architecture

```
global-geopolitical-war-room/
│
├── api/
│   └── index.py         # Vercel serverless entrypoint (re-exports FastAPI app)
│
├── backend/
│   ├── main.py          # FastAPI server, route orchestration & static mounting
│   ├── config.py        # Mode manager (mock vs live) & environment loader
│   ├── mock_data.py     # Local Mock Intelligence dataset & scenario generator
│   ├── warroom.py       # Pydantic schemas & scan execution engine
│   ├── database.py      # SQLite historical persistence & delta comparator (serverless-safe)
│   └── prompts.py       # System & user prompt templates for live mode
│
├── frontend/
│   ├── index.html       # Institutional command HUD & intelligence cards
│   ├── style.css        # Dark institutional theme, radar scanner & telemetry
│   └── app.js           # Mode telemetry, Leaflet GIS map & dynamic rendering
│
├── data/
│   └── warroom_history.db # SQLite historical runs database (local dev)
│
├── .env                 # Environment configuration (active, git-ignored)
├── .env.example         # Environment template
├── .dockerignore        # Docker build exclusions
├── Dockerfile           # Production container definition (non-root, healthchecked)
├── docker-compose.yml   # Multi-container / production orchestration with persistent volumes
├── DEPLOYMENT.md        # Comprehensive cloud & container deployment guide
├── vercel.json          # Vercel serverless configuration
├── requirements.txt     # Python dependencies
└── README.md            # Documentation & operational guide
```

---

## 🛡️ 1. Operating Modes: Mock Mode vs. Live AI Mode

The application supports two operating modes configured via the `WAR_ROOM_MODE` setting in `.env`:

### A. Mock Mode (`WAR_ROOM_MODE=mock`) — **DEFAULT**
* **Zero API Credits Required**: Does not call OpenAI API or consume billing credits.
* **100% Offline / Local Operation**: Requires no internet connectivity or OpenAI API key.
* **Rich Demonstration Intelligence**:
  - **4 Geopolitical Flashpoints**: US–Iran / Hormuz, Russia–Ukraine, US–China Tech Decoupling, India Energy Security & USD/INR Sensitivity.
  - **6-Stage Lifecycle System**: `NEW_SHOCK`, `ESCALATION`, `FULL_IMPACT`, `STABILISATION`, `RECOVERY`, `STRUCTURAL`.
  - **10-Asset Matrix**: Gold, Silver, Brent Crude, WTI Crude, DXY, EUR/USD, GBP/USD, USD/INR, NIFTY 50, BANK NIFTY.
  - **3-Scenario Engine**: Base Case, Escalation Case, De-escalation Case with invalidation criteria.
  - **Tactical GIS Heatmap**: Interactive Leaflet map with naval chokepoints and conflict zones.
  - **90-Second YouTube Teleprompter Script**: Formatted scene-by-scene script with copy-to-clipboard.
  - **Strategic Watchlist & Official Disclaimer**.

### B. Live AI Mode (`WAR_ROOM_MODE=live`)
* Requires a valid `OPENAI_API_KEY` with access to `gpt-4o`.
* Queries live web search preview to synthesize real-time open-source intelligence.

---

## 🚀 2. Quick Start Guide

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Configure `.env`
Make sure `.env` contains:
```env
WAR_ROOM_MODE=mock
```
*(If the `WAR_ROOM_MODE` setting is omitted, the application automatically defaults to `mock` mode.)*

### Step 3: Start the Server
Launch the FastAPI server using Uvicorn:
```powershell
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
Or start directly with Python:
```powershell
python backend/main.py
```

### Step 4: Open the Web Dashboard
Navigate to:
* **Web Application**: [http://localhost:8000](http://localhost:8000)
* **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Endpoint**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 3. API Verification & Testing

### 1. Check System Health
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```
**Response:**
```json
{
  "status": "ok",
  "mode": "mock"
}
```

### 2. Check Operational Mode
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/mode" -Method Get
```
**Response:**
```json
{
  "status": "ok",
  "mode": "mock",
  "is_mock": true,
  "description": "Local Mock Intelligence Mode (No OpenAI API credits or internet required)"
}
```

### 3. Run War Room Intelligence Scan
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/run" -Method Post
```
*(Returns full structured JSON dossier with mode, report_id, executive_summary, geopolitical_events, asset_impact, scenarios, watchlist, video_script, disclaimer, and hotspots.)*

### 4. Fetch Baseline Theaters
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/theaters/baseline" -Method Get
```

---

## 🔄 4. How to Switch to Live AI Mode Later

When you are ready to use live OpenAI credits:

1. Open `.env` in the project root:
   ```env
   WAR_ROOM_MODE=live
   OPENAI_API_KEY=sk-proj-your-valid-api-key-here
   OPENAI_MODEL=gpt-4o
   ```
2. Restart the server:
   ```powershell
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. The HUD header will automatically display `LIVE AI MODE — OPENAI OSINT` and make live web-search calls.

---

## 🔒 5. Security & Isolation Guarantee

* **API Key Safety**: API keys are never exposed in HTML, client JavaScript, or API mode endpoints.
* **Mock Mode Safety**: When `WAR_ROOM_MODE=mock`, the OpenAI SDK is never instantiated, avoiding network requests, 429 quota errors, or token billing.
* **Production Docs**: Swagger UI and ReDoc are disabled on Vercel to avoid leaking internal API schema.

---

## ☁️ 6. Vercel Public Deployment

### Files Added for Vercel

| File | Purpose |
|---|---|
| `api/index.py` | Vercel serverless entrypoint — bootstraps `sys.path` and exports the FastAPI `app` |
| `vercel.json` | Routing configuration — maps static assets and API routes |
| `.gitignore` | Excludes `.env`, local DB, and Python cache from the repository |

### Step 1: Prepare GitHub Repository

```bash
# Initialise Git in the project directory
git init
git add .
git commit -m "Initial commit: Global Geopolitical War Room with Vercel deployment"

# Create a repository on GitHub, then push
git remote add origin https://github.com/YOUR_USERNAME/global-geopolitical-war-room.git
git branch -M main
git push -u origin main
```

> **Important**: The `.gitignore` excludes `.env`. **Never commit your real `.env` file.**

### Step 2: Deploy on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub.
2. Click **Add New → Project**.
3. Select your `global-geopolitical-war-room` repository.
4. Vercel auto-detects Python — accept the default build settings.
5. Set the following **Environment Variables** in the Vercel dashboard:

| Variable | Value | Required |
|---|---|---|
| `WAR_ROOM_MODE` | `mock` | ✅ Yes |
| `OPENAI_API_KEY` | *(leave blank or omit)* | ❌ Not needed for Mock Mode |

6. Click **Deploy**. Vercel will build and deploy.

### Step 3: Verify the Deployment

Once deployed, test these endpoints at your Vercel URL:

```
GET  https://your-project.vercel.app/             → HTML dashboard
GET  https://your-project.vercel.app/health        → {"status":"ok","mode":"mock"}
GET  https://your-project.vercel.app/api/mode      → {"mode":"mock","is_mock":true,...}
POST https://your-project.vercel.app/api/run       → Full mock intelligence dossier
```

### Known Serverless Limitations

| Limitation | Impact | Mitigation |
|---|---|---|
| **Read-only filesystem** | SQLite writes to `/tmp` (ephemeral) | History resets on cold start; acceptable for demo |
| **No persistent storage** | `/api/history` returns empty on Vercel | Use an external DB (Supabase/PlanetScale) for production history |
| **Cold starts** | First request may take 3–5 seconds | Normal for Python serverless; subsequent requests are fast |
| **50MB lambda limit** | Large `mock_data.py` is fine; live mode with large models may be slow | Only `mock` mode enabled by default |
| **No file writes** | Database in `/tmp` is not shared across function instances | Acceptable for stateless demo deployments |

### Switching to Live AI Mode on Vercel (Optional)

1. Ensure you have a valid OpenAI API key with credits.
2. In Vercel dashboard → **Settings → Environment Variables**, set:
   - `WAR_ROOM_MODE` = `live`
   - `OPENAI_API_KEY` = `sk-proj-your-real-key`
3. **Redeploy** the project.

> ⚠️ Live mode makes real OpenAI API calls and consumes billing credits.

---

## 🧪 7. Running Tests

```powershell
# Run backend integration tests
python backend/test_warroom.py

# Verify zero-key mock mode
python backend/test_zero_key.py
```

---

## 🗄️ 8. Historical Comparison Engine (Local Only)

The comparison engine works fully in local development. On Vercel, history is ephemeral (resets on cold start):

```powershell
# Seed sample historical runs
Invoke-RestMethod -Uri "http://localhost:8000/api/history/seed-samples" -Method Post

# List all runs
Invoke-RestMethod -Uri "http://localhost:8000/api/history" -Method Get

# Compare two runs
Invoke-RestMethod -Uri "http://localhost:8000/api/history/compare/1/2" -Method Get
```

---

## 🚀 9. Production Deployment

See [DEPLOYMENT.md](file:///c:/Users/Abcom/.gemini/antigravity-ide/scratch/global-geopolitical-war-room/DEPLOYMENT.md) for complete instructions.

### Docker Compose (One-Click)
```bash
docker-compose up -d
```

### Vercel Serverless
```bash
vercel --prod
```


