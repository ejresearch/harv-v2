# Quick fix script for main.py
cat >> fix_main.sh << 'EOF'
#!/bin/bash
echo "🔧 Fixing main.py to include API router..."

# Check if api_router import exists
if ! grep -q "from .api.v1.api import api_router" backend/app/main.py; then
    echo "Adding api_router import..."
    # Add import after other imports
    sed -i '/from .core.database import create_tables/a from .api.v1.api import api_router' backend/app/main.py
fi

# Check if include_router exists  
if ! grep -q "app.include_router.*api_router" backend/app/main.py; then
    echo "Adding router inclusion..."
    # Add router inclusion after app creation
    sed -i '/^app = FastAPI(/a\\napp.include_router(api_router, prefix="/api/v1")' backend/app/main.py
fi

echo "✅ main.py updated!"
echo "🔄 Now restart your server:"
echo "   cd backend && uvicorn app.main:app --reload --port 8000"
EOF

chmod +x fix_main.sh
./fix_main.sh
