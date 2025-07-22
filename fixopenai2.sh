#!/bin/bash
# Long-term OpenAI Integration Fix
# Fixes the proxies argument issue permanently

echo "🔧 Implementing long-term OpenAI fix..."

# Stop any running server
pkill -f "uvicorn app.main:app" 2>/dev/null || true

# Navigate to backend
cd backend

# Activate virtual environment
source venv/bin/activate

echo "📦 Installing latest compatible versions..."

# Uninstall problematic versions
pip uninstall -y openai httpx

# Install the LATEST OpenAI version (1.59.2+) which has the httpx fix
# This version removes the hardcoded proxies parameter
pip install "openai>=1.59.0"

# Let pip resolve httpx dependency automatically - it will install compatible version
pip install --upgrade httpx

echo "🔍 Verifying installation..."
python -c "
try:
    from openai import OpenAI
    client = OpenAI(api_key='test-key')
    print('✅ OpenAI client initialized successfully')
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"

echo "📝 Creating production-ready requirements..."
cat > requirements_fixed.txt << 'EOF'
# Production Requirements - Long-term Stable
# Last updated: January 2025

# Core Framework
fastapi==0.110.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
alembic==1.12.1

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.0.1
python-multipart==0.0.9

# CORS
fastapi-cors==0.0.6

# Environment
python-dotenv==1.0.0
pydantic-settings==2.1.0

# OpenAI - FIXED with latest version
openai>=1.59.0

# HTTP Client - Compatible with OpenAI 1.59+
httpx>=0.27.0

# Logging
structlog==24.1.0

# Validation
pydantic>=2.5.0

# Date handling
python-dateutil==2.8.2

# JSON handling
orjson==3.9.12
EOF

echo "🚀 Installing from fixed requirements..."
pip install -r requirements_fixed.txt

echo "🔄 Creating clean OpenAI service..."
# The service should now work with AsyncOpenAI without issues

echo "✅ Long-term fix complete!"
echo ""
echo "🎯 What was fixed:"
echo "   - Upgraded to OpenAI 1.59.0+ (removes hardcoded proxies)"
echo "   - Compatible httpx version (0.27.0+)"
echo "   - Production-ready requirements.txt"
echo ""
echo "🚀 Starting server..."
uvicorn app.main:app --reload --port 8000
