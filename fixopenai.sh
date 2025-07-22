#!/bin/bash
# Quick fix for OpenAI integration issues

echo "🔧 Fixing OpenAI integration compatibility issues..."

# Navigate to backend
cd backend

# Uninstall problematic OpenAI version
echo "📦 Uninstalling current OpenAI version..."
pip uninstall -y openai

# Install compatible version
echo "📦 Installing compatible OpenAI version..."
pip install openai==1.51.2

# Upgrade httpx to compatible version
echo "📦 Updating httpx..."
pip install --upgrade httpx==0.26.0

# Restart the server
echo "🚀 Restarting server..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
sleep 2

# Start server in background
uvicorn app.main:app --reload --port 8000 &

echo "✅ Fix complete! Server should be running on port 8000"
echo "Test with: curl http://localhost:8000/api/v1/memory/health"
