# ==============================================================================
# Global Geopolitical War Room - Production Container Image
# Multi-arch ready, security-hardened, non-root execution
# ==============================================================================

FROM python:3.12-slim-bookworm AS base

# Prevent Python from writing .pyc files and enable unbuffered streaming logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000 \
    WAR_ROOM_MODE=mock

# Set work directory
WORKDIR /app

# Install security updates & curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies in a dedicated layer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create application user and set up directories with correct permissions
RUN groupadd -g 1001 warroom && \
    useradd -u 1001 -g warroom -s /bin/bash -m warroom && \
    mkdir -p /app/data /app/backend /app/frontend /app/api && \
    chown -R warroom:warroom /app

# Copy application source code
COPY --chown=warroom:warroom backend/ /app/backend/
COPY --chown=warroom:warroom frontend/ /app/frontend/
COPY --chown=warroom:warroom api/ /app/api/
COPY --chown=warroom:warroom .env.example /app/.env.example

# Switch to non-root execution
USER warroom

# Expose HTTP port
EXPOSE 8000

# Docker Healthcheck to verify system readiness
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Launch production ASGI server
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--no-access-log"]
