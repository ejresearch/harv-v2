# Deployment Guide

## Production Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f
```

### Manual Deployment

```bash
# Set production environment
export DATABASE_URL="postgresql://user:pass@host:5432/harv_prod"
export SECRET_KEY="your-production-secret-key"
export DEBUG=false

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start with Gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | Database connection string |
| SECRET_KEY | Yes | JWT signing key |
| OPENAI_API_KEY | Yes | OpenAI API key |
| DEBUG | No | Debug mode (default: false) |
| CORS_ORIGINS | No | Allowed CORS origins |

### Health Checks

- `GET /health` - Basic health check
- `GET /health/database` - Database connectivity
- `GET /health/detailed` - Comprehensive status

### Monitoring

Recommended monitoring setup:
- Application logs: Structured JSON logging
- Metrics: Prometheus/Grafana
- Error tracking: Sentry
- Uptime monitoring: Health check endpoints
