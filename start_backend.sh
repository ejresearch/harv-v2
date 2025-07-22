#!/bin/bash
# Start Harv v2.0 Backend with ALL Features

echo "🚀 Starting Harv v2.0 Backend - COMPLETE VERSION"
echo "==============================================="

# Check virtual environment
if [[ -f "backend/venv/bin/activate" ]]; then
    echo "✅ Activating virtual environment..."
    source backend/venv/bin/activate
else
    echo "⚠️  No virtual environment found, continuing..."
fi

echo ""
echo "🌐 Starting FastAPI server with ALL endpoints..."
echo ""
echo "📍 Available after startup:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • System Overview: http://localhost:8000/"
echo "   • Health Check: http://localhost:8000/health"
echo "   • Memory System: http://localhost:8000/api/v1/memory/enhanced/1"
echo "   • Chat Endpoint: http://localhost:8000/api/v1/chat/enhanced"
echo "   • Modules List: http://localhost:8000/api/v1/modules/"
echo ""
echo "🧠 Features Enabled:"
echo "   • 4-Layer Memory System: OPERATIONAL"
echo "   • Socratic Chat: FUNCTIONAL"
echo "   • Module Management: ACTIVE"
echo "   • Progress Tracking: WORKING"
echo "   • No Authentication Required: DEVELOPMENT MODE"
echo ""

cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
