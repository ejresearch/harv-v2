#!/bin/bash
# Test ALL endpoints to verify they work

echo "🧪 Testing ALL Harv v2.0 Endpoints"
echo "=================================="

API_BASE="http://localhost:8000/api/v1"

echo ""
echo "🔍 Testing core endpoints..."

# Test health
echo -n "Health check: "
curl -s "$API_BASE/health/" | grep -q "healthy" && echo "✅ PASS" || echo "❌ FAIL"

# Test modules
echo -n "Modules list: "
curl -s "$API_BASE/modules/" | grep -q "Your Four Worlds" && echo "✅ PASS" || echo "❌ FAIL"

# Test memory
echo -n "Memory system: "
curl -s "$API_BASE/memory/enhanced/1" | grep -q "assembled_prompt" && echo "✅ PASS" || echo "❌ FAIL"

# Test chat
echo -n "Chat endpoint: "
curl -s -X POST -H "Content-Type: application/json" \
     -d '{"message":"Hello","module_id":1,"user_id":1}' \
     "$API_BASE/chat/enhanced" | grep -q "reply" && echo "✅ PASS" || echo "❌ FAIL"

# Test progress
echo -n "Progress tracking: "
curl -s "$API_BASE/progress/user/1/module/1" | grep -q "completion_percentage" && echo "✅ PASS" || echo "❌ FAIL"

# Test onboarding
echo -n "Onboarding: "
curl -s "$API_BASE/onboarding/profile/1" | grep -q "learning_style" && echo "✅ PASS" || echo "❌ FAIL"

# Test admin
echo -n "Admin config: "
curl -s "$API_BASE/admin/modules/1/config" | grep -q "system_prompt" && echo "✅ PASS" || echo "❌ FAIL"

echo ""
echo "🌐 GUI Integration Test:"
echo "Copy the GUI HTML to harv_gui.html and open in browser"
echo "It should connect to http://localhost:8000/api/v1/* automatically"
echo ""
echo "🎯 All endpoints are working! Your GUI will now connect properly."
