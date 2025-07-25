#!/bin/bash
# Quick start script for Harv v2.0 demo

echo "🚀 Starting Harv v2.0 Dual-Perspective Demo"
echo "========================================"

# Navigate to backend
cd backend

# Setup demo data
echo "📊 Setting up demo data..."
python setup_demo_data.py

echo ""
echo "🌐 Starting server..."
echo "Demo will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
