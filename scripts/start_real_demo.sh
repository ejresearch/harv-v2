#!/bin/bash
# Start Harv v2.0 with 100% Real Metrics Demo

echo "🎯 HARV v2.0 - REAL PERFORMANCE DEMO STARTUP"
echo "============================================="
echo "Starting fully functional demo with:"
echo "  • Real database metrics"
echo "  • Live memory system performance"
echo "  • WebSocket real-time updates"
echo "  • Actual API response tracking"
echo ""

# Activate virtual environment
if [[ -f "venv/bin/activate" ]]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found"
    echo "Run: python -m venv venv && source venv/bin/activate"
    exit 1
fi

# Install/update dependencies
echo "📦 Installing real-time monitoring dependencies..."
pip install -r backend/requirements.txt

# Create real demo data
echo ""
echo "🌱 Setting up real demo data..."
cd backend
python create_real_demo_data.py

# Run database migrations if needed
echo "📊 Ensuring database is ready..."
python -c "from app.core.database import create_tables; create_tables()"

# Start the server
echo ""
echo "🎬 STARTING HARV v2.0 REAL DEMO SERVER"
echo "====================================="
echo ""
echo "🎯 Real Demo Features:"
echo "   • Real Database: SQLite with actual data"
echo "   • Real Metrics: /api/v1/metrics/live"
echo "   • Real Memory: /api/v1/memory/enhanced/{module_id}"
echo "   • Real Chat: /api/v1/chat/enhanced"
echo "   • Real SQL: /api/v1/metrics/sql-activity"
echo "   • WebSocket: ws://localhost:8000/api/v1/metrics/live-metrics"
echo ""
echo "📱 Demo Login: demo@harv.com / demo123"
echo "🌐 Server: http://localhost:8000"
echo "📊 API Docs: http://localhost:8000/docs"
echo ""
echo "🔥 NO FAKE DATA - EVERYTHING IS REAL!"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
