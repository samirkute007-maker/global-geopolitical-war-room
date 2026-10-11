# 🚀 Production Deployment & Operations Guide
## Global Geopolitical War Room v3.0

This guide covers production deployment options for the **Global Geopolitical War Room**, including Docker containerization, Docker Compose, Cloud Serverless (Vercel), and major Cloud PaaS providers (Railway, Render, Fly.io, AWS).

---

## ⚙️ Environment Variables Reference

| Variable | Type | Default | Description |
|---|---|---|---|
| `WAR_ROOM_MODE` | String | `live` | Operation mode: `live` (Real-Time OSINT engine) or `mock` (Deterministic sample data). |
| `OPENAI_API_KEY` | String | _(Optional)_ | OpenAI API key for LLM-driven intelligence enrichment. If omitted or quota-limited, system automatically uses zero-key Public Live OSINT Engine with zero downtime. |
| `WARROOM_LLM_MODEL`| String | `gpt-4o` | Model identifier if OpenAI is configured (e.g., `gpt-4o`, `gpt-4o-mini`). |
| `PORT` | Integer | `8000` | Port for the HTTP / ASGI server. |

---

## 🐳 Option 1: Docker Container Deployment (Recommended)

### Build the Image
```bash
docker build -t global-geopolitical-war-room:v3.0 .
```

### Run the Container
```bash
docker run -d \
  --name geopolitical-war-room \
  -p 8000:8000 \
  -e WAR_ROOM_MODE=live \
  -v warroom_data:/app/data \
  --restart unless-stopped \
  global-geopolitical-war-room:v3.0
```

### Verify Container Health
```bash
docker ps
curl http://localhost:8000/health
```

---

## 📦 Option 2: Docker Compose (One-Click Production Spin-Up)

A pre-configured `docker-compose.yml` is included with health checks, persistent data volumes, and restart policies.

```bash
# Start in detached background mode
docker-compose up -d

# View live logs
docker-compose logs -f war-room

# Stop service
docker-compose down
```

---

## ☁️ Option 3: Vercel Serverless Deployment

The project is structured with native Vercel Python runtime support via `api/index.py` and `vercel.json`.

### Deploy using Vercel CLI
```bash
# Install Vercel CLI if needed
npm i -g vercel

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Serverless Architecture Notes
- **Static Assets**: Automatically served via Vercel's global Edge CDN (`/frontend/*`, `/style.css`, `/app.js`).
- **Dynamic API**: Handled serverlessly by `api/index.py` (FastAPI / ASGI).
- **Storage**: In read-only serverless environments, SQLite seamlessly falls back to `/tmp/warroom_history.db` with full fault tolerance.

---

## 🚀 Option 4: Cloud PaaS (Railway, Render, Fly.io)

### Railway
1. Connect your GitHub repository to [Railway](https://railway.app).
2. Railway will automatically detect the `Dockerfile`.
3. Add environment variables: `WAR_ROOM_MODE=live`.
4. Attach a persistent volume at `/app/data` for historical archive persistence.

### Render
1. Create a new **Web Service** on [Render](https://render.com).
2. Choose **Docker** as the runtime.
3. Set disk mount path to `/app/data`.
4. Set Health Check path to `/health`.

### Fly.io
```bash
fly launch
fly deploy
```

---

## 🔍 Health Checks & Operational Diagnostics

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | `GET` | Container / load balancer liveness probe. Returns `{ "status": "ok", "app": "..." }`. |
| `/api/mode` | `GET` | Returns active operation mode (`live` vs `mock`) and active data provider. |
| `/api/credits/check` | `GET` | Inspects LLM quota status and OSINT engine connectivity. |
| `/api/history` | `GET` | Returns count and summary of all archived intelligence runs. |

---

## 🛡️ Security Best Practices
1. The `Dockerfile` runs as a dedicated non-root user (`UID 1001 / warroom`).
2. Live OSINT scrapers execute with strict timeouts (10s per feed) to prevent connection starvation.
3. CORS headers are configured for secure browser communication.
