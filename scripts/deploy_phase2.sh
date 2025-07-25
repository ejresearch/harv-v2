#!/bin/bash
# Phase 2 Deployment Script
# Deploys enhanced memory system to production

echo "🚀 Deploying Phase 2: Enhanced Memory System"
echo "============================================"

# Activate virtual environment
if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
elif [[ -f "backend/venv/bin/activate" ]]; then
    source backend/venv/bin/activate
    echo "✅ Backend virtual environment activated"
else
    echo "❌ Virtual environment not found"
    exit 1
fi

# Install any new dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r backend/requirements.txt

# Run database migrations
echo ""
echo "📊 Running memory system migrations..."
python backend/migrate_memory_system.py

if [[ $? -eq 0 ]]; then
    echo "✅ Database migration successful"
else
    echo "❌ Database migration failed"
    exit 1
fi

# Run tests
echo ""
echo "🧪 Running memory system tests..."
python -m pytest backend/tests/test_memory_system.py -v

if [[ $? -eq 0 ]]; then
    echo "✅ All tests passed"
else
    echo "⚠️  Some tests failed - review before production deployment"
fi

# Start the server
echo ""
echo "🚀 Starting Harv v2.0 with Enhanced Memory System..."
echo "Server will be available at:"
echo "  - Main API: http://localhost:8000"
echo "  - Documentation: http://localhost:8000/docs"
echo "  - Memory Health: http://localhost:8000/api/v1/memory/health"
echo ""

# Change to backend directory for uvicorn
cd backend

# Start server with production settings
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info \
    --access-log \
    --loop asyncio

echo "🎉 Phase 2 Enhanced Memory System Deployed!"
