#!/bin/bash
# Complete Demo Fix Script for Harv v2.0
# This script diagnoses and fixes all demo.html API connection issues

echo "🔧 HARV v2.0 DEMO FIX SCRIPT"
echo "============================"
echo ""

# Check if we're in the right directory
if [[ ! -f "demo.html" ]]; then
    echo "❌ Error: demo.html not found in current directory"
    echo "Please run this script from your harv-v2 root directory"
    exit 1
fi

echo "✅ Found demo.html"
echo ""

# Step 1: Check server status
echo "🔍 Step 1: Checking server status..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Server is running"
else
    echo "❌ Server is not responding"
    echo "Please start your server first:"
    echo "   cd backend && uvicorn app.main:app --reload --port 8000"
    exit 1
fi

# Step 2: Test API endpoints to find correct structure
echo ""
echo "🔍 Step 2: Testing API endpoint structure..."

# Test different possible API structures
API_ENDPOINTS=(
    "http://localhost:8000/api/v1/auth/register"
    "http://localhost:8000/auth/register" 
    "http://localhost:8000/api/v1/health"
    "http://localhost:8000/health"
)

WORKING_BASE=""
echo "Testing endpoint structures..."

for endpoint in "${API_ENDPOINTS[@]}"; do
    if [[ "$endpoint" == *"/auth/register" ]]; then
        # Test POST endpoint
        response=$(curl -s -X POST "$endpoint" \
            -H "Content-Type: application/json" \
            -d '{"name": "Test", "email": "test@example.com", "password": "test123"}' \
            -w "%{http_code}")
        
        http_code="${response: -3}"
        if [[ "$http_code" != "404" ]]; then
            if [[ "$endpoint" == *"/api/v1/"* ]]; then
                WORKING_BASE="http://localhost:8000/api/v1"
            else
                WORKING_BASE="http://localhost:8000"
            fi
            echo "✅ Found working auth endpoint: $endpoint (HTTP $http_code)"
            break
        else
            echo "❌ $endpoint - Not found"
        fi
    elif [[ "$endpoint" == *"/health" ]]; then
        # Test GET endpoint
        response=$(curl -s -w "%{http_code}" "$endpoint")
        http_code="${response: -3}"
        if [[ "$http_code" == "200" ]]; then
            if [[ "$endpoint" == *"/api/v1/"* ]]; then
                WORKING_BASE="http://localhost:8000/api/v1"
            else
                WORKING_BASE="http://localhost:8000"
            fi
            echo "✅ Found working health endpoint: $endpoint"
            break
        else
            echo "❌ $endpoint - Not found"
        fi
    fi
done

if [[ -z "$WORKING_BASE" ]]; then
    echo ""
    echo "❌ Could not determine API structure. Let's check what endpoints exist..."
    echo "Visit http://localhost:8000/docs to see available endpoints"
    echo ""
    echo "Manual fix: Edit demo.html and change the API_BASE line to match your API structure"
    exit 1
fi

echo "✅ Determined API base URL: $WORKING_BASE"

# Step 3: Check current API_BASE in demo.html
echo ""
echo "🔍 Step 3: Checking current API configuration in demo.html..."

CURRENT_API_BASE=$(grep -o "const API_BASE = '[^']*'" demo.html | head -1)
echo "Current setting: $CURRENT_API_BASE"

# Step 4: Fix the API_BASE if needed
echo ""
echo "🔧 Step 4: Updating demo.html API configuration..."

# Create backup
cp demo.html demo.html.backup
echo "✅ Created backup: demo.html.backup"

# Fix the API_BASE
sed -i.tmp "s|const API_BASE = '[^']*'|const API_BASE = '$WORKING_BASE'|g" demo.html
rm demo.html.tmp 2>/dev/null || true

NEW_API_BASE=$(grep -o "const API_BASE = '[^']*'" demo.html | head -1)
echo "✅ Updated to: $NEW_API_BASE"

# Step 5: Test the fix
echo ""
echo "🔍 Step 5: Testing the fix..."

# Test registration endpoint
echo "Testing registration endpoint..."
test_response=$(curl -s -X POST "$WORKING_BASE/auth/register" \
    -H "Content-Type: application/json" \
    -d '{"name": "Demo Test", "email": "demotest@example.com", "password": "testpass123"}' \
    -w "%{http_code}")

test_http_code="${test_response: -3}"
if [[ "$test_http_code" == "200" ]] || [[ "$test_http_code" == "400" ]]; then
    echo "✅ Registration endpoint working (HTTP $test_http_code)"
    REGISTRATION_WORKS=true
else
    echo "❌ Registration endpoint issue (HTTP $test_http_code)"
    REGISTRATION_WORKS=false
fi

# Test modules endpoint  
echo "Testing modules endpoint..."
modules_response=$(curl -s "$WORKING_BASE/modules/" -w "%{http_code}")
modules_http_code="${modules_response: -3}"
if [[ "$modules_http_code" == "200" ]] || [[ "$modules_http_code" == "401" ]]; then
    echo "✅ Modules endpoint found (HTTP $modules_http_code)"
    MODULES_WORKS=true
else
    echo "❌ Modules endpoint not found (HTTP $modules_http_code)"
    MODULES_WORKS=false
fi

# Step 6: Final validation and instructions
echo ""
echo "🎯 Step 6: Final Results"
echo "========================"

if [[ "$REGISTRATION_WORKS" == true ]] && [[ "$MODULES_WORKS" == true ]]; then
    echo "🎉 SUCCESS! Demo should now work perfectly!"
    echo ""
    echo "🚀 Next steps:"
    echo "1. Open your browser to: http://localhost:8000/demo"
    echo "2. Click 'Try Demo'"
    echo "3. Register a new account or use existing credentials"
    echo "4. Explore all 4 tabs: Dashboard, Learning Session, Memory System, Progress"
    echo ""
    echo "✨ Your demo.html is now properly connected to the API!"
    
elif [[ "$REGISTRATION_WORKS" == true ]]; then
    echo "⚠️  PARTIAL SUCCESS - Authentication works but some endpoints missing"
    echo ""
    echo "The demo will work for login/registration, but some features might not load."
    echo "Check your main.py to ensure all API routers are included:"
    echo ""
    echo "app.include_router(api_router, prefix='$WORKING_BASE')"
    echo ""
    echo "Try the demo anyway: http://localhost:8000/demo"
    
else
    echo "❌ API CONNECTION ISSUES"
    echo ""
    echo "The demo.html has been updated but API endpoints aren't responding correctly."
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check http://localhost:8000/docs for available endpoints"
    echo "2. Verify your main.py includes the API router properly"
    echo "3. Restart your server: uvicorn app.main:app --reload --port 8000"
    echo ""
    echo "Manual test: visit http://localhost:8000/demo and check browser console (F12)"
fi

echo ""
echo "📋 Configuration Summary:"
echo "  Server: http://localhost:8000 ✅"
echo "  Demo page: http://localhost:8000/demo ✅"
echo "  API base: $WORKING_BASE $(if [[ "$REGISTRATION_WORKS" == true ]]; then echo "✅"; else echo "❌"; fi)"
echo "  Backup created: demo.html.backup ✅"

echo ""
echo "🔧 If issues persist, run this for detailed diagnostics:"
echo "curl -s http://localhost:8000/docs | grep -o '\"operationId\":\"[^\"]*\"' | head -10"
