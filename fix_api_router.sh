#!/bin/bash
echo "🔧 Adding API router to main.py..."

cd backend/app

# Check if the import exists
if ! grep -q "from .api.v1.api import api_router" main.py; then
    echo "Adding api_router import..."
    # Add import after the database import line
    sed -i '/from .core.database import create_tables/a from .api.v1.api import api_router' main.py
fi

# Check if the router inclusion exists
if ! grep -q "app.include_router.*api_router" main.py; then
    echo "Adding router inclusion..."
    # Find where the app is defined and add the router after middleware
    sed -i '/app.add_middleware(/a\\n# Include all API endpoints\napp.include_router(api_router, prefix="/api/v1")' main.py
fi

echo "✅ main.py updated!"
echo ""
echo "🔄 Please restart your server now:"
echo "   Press Ctrl+C to stop current server"  
echo "   Then run: uvicorn app.main:app --reload --port 8000"
