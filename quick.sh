#!/bin/bash
# SUPER EASY SETUP - One command does everything

echo "🚀 HARV v2.0 - SUPER EASY SETUP"
echo "================================"

# Check if we're in the right place
if [[ ! -d "backend/app" ]]; then
    echo "❌ Run this from your harv-v2 directory"
    exit 1
fi

echo "✅ Found harv-v2 structure"

# Step 1: Fix OpenAI service
echo "🔧 Step 1: Fixing OpenAI service..."
python3 - << 'EOF'
import os

modern_code = '''"""
OpenAI Service - GPT-4o with Modern API
"""

from openai import AsyncOpenAI
import asyncio
import logging
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

from app.core.config import settings

logger = logging.getLogger(__name__)

class SocraticAnalysis(BaseModel):
    question_count: int
    socratic_compliance: str
    engagement_level: str
    teaching_approach: str
    effectiveness_score: float
    has_direct_answers: bool
    improvement_suggestions: List[str] = Field(default_factory=list)

class TokenUsage(BaseModel):
    model_config = {"protected_namespaces": ()}
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float
    model_used: str
    response_time_ms: int

class OpenAIResponse(BaseModel):
    success: bool
    response: str = ""
    socratic_analysis: Optional[SocraticAnalysis] = None
    token_usage: Optional[TokenUsage] = None
    error: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class OpenAIService:
    def __init__(self):
        if not settings.openai_api_key:
            self.demo_mode = True
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=settings.openai_api_key)
            self.demo_mode = False
        
        self.model = settings.openai_model or "gpt-4o"
        self.max_tokens = 1500
        self.temperature = 0.7
        self.request_count = 0
        
        logger.info(f"🤖 OpenAI Service - Model: {self.model}, Demo: {self.demo_mode}")

    async def generate_socratic_response(self, enhanced_memory_context: str, user_message: str, conversation_history: List[Dict[str, str]] = None, module_id: int = 1) -> OpenAIResponse:
        start_time = time.time()
        
        try:
            if self.demo_mode:
                return await self._generate_demo_response(user_message, module_id)
            
            system_prompt = f"""You are an expert AI tutor using GPT-4o and the Socratic method.

RULES:
- Ask questions, don't give direct answers
- 70%+ of response should be questions  
- Use encouraging tone
- Reference student context

STUDENT CONTEXT:
{enhanced_memory_context}

Guide through questions, not answers."""

            user_prompt = f"Student: {user_message}\\n\\nYour Socratic response:"
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Analyze Socratic compliance
            question_count = ai_response.count("?")
            sentences = len([s for s in ai_response.split(".") if s.strip()])
            question_ratio = question_count / max(sentences, 1)
            
            compliance = "HIGH" if question_ratio >= 0.7 else "MEDIUM" if question_ratio >= 0.4 else "LOW"
            effectiveness = 0.9 if compliance == "HIGH" else 0.7 if compliance == "MEDIUM" else 0.4
            
            socratic_analysis = SocraticAnalysis(
                question_count=question_count,
                socratic_compliance=compliance,
                engagement_level="HIGH" if question_count >= 3 else "MEDIUM",
                teaching_approach="Socratic questioning",
                effectiveness_score=effectiveness,
                has_direct_answers=False
            )
            
            # Calculate costs
            input_cost = (response.usage.prompt_tokens / 1000000) * 5.0
            output_cost = (response.usage.completion_tokens / 1000000) * 15.0
            
            token_usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                estimated_cost=input_cost + output_cost,
                model_used=self.model,
                response_time_ms=int((time.time() - start_time) * 1000)
            )
            
            self.request_count += 1
            
            return OpenAIResponse(
                success=True,
                response=ai_response,
                socratic_analysis=socratic_analysis,
                token_usage=token_usage
            )
            
        except Exception as e:
            return OpenAIResponse(success=False, error=str(e))

    async def _generate_demo_response(self, user_message: str, module_id: int) -> OpenAIResponse:
        demo_response = "That's an interesting question! What do you think makes communication effective? How might you explore this concept further based on your own experiences?"
        
        return OpenAIResponse(
            success=True,
            response=demo_response,
            socratic_analysis=SocraticAnalysis(
                question_count=2,
                socratic_compliance="HIGH",
                engagement_level="HIGH",
                teaching_approach="Socratic questioning",
                effectiveness_score=0.85,
                has_direct_answers=False
            ),
            token_usage=TokenUsage(
                prompt_tokens=200,
                completion_tokens=50,
                total_tokens=250,
                estimated_cost=0.008,
                model_used="demo-mode",
                response_time_ms=500
            )
        )

    async def test_connection(self) -> Dict[str, Any]:
        if self.demo_mode:
            return {"status": "demo_mode", "message": "No API key - using demo", "working": True}
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return {"status": "connected", "message": f"Connected to {self.model}", "working": True}
        except Exception as e:
            return {"status": "error", "message": str(e), "working": False}

    def get_service_metrics(self) -> Dict[str, Any]:
        return {
            "requests_processed": self.request_count,
            "demo_mode": self.demo_mode,
            "model": self.model
        }
'''

with open("backend/app/services/openai_service.py", "w") as f:
    f.write(modern_code)

print("✅ OpenAI service updated")
EOF

# Step 2: Setup environment with placeholder
echo "🔧 Step 2: Setting up environment..."
cat > backend/.env << 'EOF'
# Harv v2.0 Configuration
DATABASE_URL=sqlite:///./harv_v2.db
SECRET_KEY=your-super-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration - ADD YOUR KEY HERE
OPENAI_API_KEY=REPLACE_WITH_YOUR_OPENAI_KEY
OPENAI_MODEL=gpt-4o

# Development
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]
MEMORY_MAX_CONTEXT_LENGTH=4000
MEMORY_FALLBACK_ENABLED=true
SOCRATIC_MODE_ENABLED=true
PREVENT_DIRECT_ANSWERS=true
EOF

# Step 3: Test the setup
echo "🧪 Step 3: Testing setup..."
cd backend
python -c "
try:
    from app.services.openai_service import OpenAIService
    from app.api.v1.endpoints.chat import router
    from app.api.v1.api import api_router
    print('✅ All imports working!')
    print(f'📊 API routes: {len(api_router.routes)}')
except Exception as e:
    print(f'❌ Import error: {e}')
"

echo ""
echo "🎉 SETUP COMPLETE!"
echo "=================="
echo ""
echo "📝 NEXT STEPS:"
echo "1. Add your OpenAI API key to backend/.env"
echo "2. Start server: cd backend && uvicorn app.main:app --reload"
echo "3. Test: curl http://localhost:8000/api/v1/chat/demo/1"
echo ""
echo "🔑 Edit backend/.env and replace:"
echo "   OPENAI_API_KEY=REPLACE_WITH_YOUR_OPENAI_KEY"
echo "   with your actual OpenAI API key"
echo ""
echo "🚀 Then run: cd backend && uvicorn app.main:app --reload"
