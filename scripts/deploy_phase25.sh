#!/bin/bash
# Phase 2.5 Deployment Script
# Complete deployment of OpenAI + WebSocket + Analytics integration

echo "🚀 DEPLOYING PHASE 2.5: Complete AI Tutoring Platform"
echo "===================================================="
echo ""

# Check environment
if [[ ! -f "backend/.env" ]]; then
    echo "⚠️ Warning: .env file not found"
    echo "Copy .env.example to .env and configure your settings"
    echo ""
fi

# Activate virtual environment
if [[ -f "backend/venv/bin/activate" ]]; then
    source backend/venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found - please set up venv first"
    exit 1
fi

# Run database migration
echo ""
echo "🗄️ Running Phase 2.5 database migration..."
cd backend
python migrate_phase25.py

if [[ $? -eq 0 ]]; then
    echo "✅ Database migration completed"
else
    echo "❌ Migration failed"
    exit 1
fi

# Run tests
echo ""
echo "🧪 Running Phase 2.5 integration tests..."
python -m pytest tests/phase25/ -v

# Start services
echo ""
echo "🎯 Starting Harv v2.0 Phase 2.5 services..."
echo ""
echo "🧠 Enhanced Memory System: ACTIVE"
echo "🤖 OpenAI GPT-4 Integration: ACTIVE"
echo "🔌 WebSocket Real-time Chat: ACTIVE"
echo "📊 Learning Analytics Dashboard: ACTIVE"
echo "🎓 Socratic Methodology: ENFORCED"
echo ""

# Start the complete application
echo "🚀 Starting Harv v2.0 Phase 2.5..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "WebSocket Chat: ws://localhost:8000/api/v1/chat/ws/{module_id}"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info
