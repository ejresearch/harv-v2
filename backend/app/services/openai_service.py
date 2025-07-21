# Phase 2.5: OpenAI Chat Integration
## Transform Memory System into Live AI Tutor

### 🎯 Phase 2.5 Mission
**Transform your brilliant 4-layer memory system from context assembly into a live, Socratic AI tutoring experience**

Your enhanced memory system is now operational and assembling perfect context. Phase 2.5 connects this to OpenAI's GPT-4 to create actual intelligent tutoring sessions.

---

## 🚀 Implementation Steps

### Step 1: OpenAI Service Integration

**Create: `backend/app/services/openai_service.py`**
```python
"""
OpenAI Chat Service - Phase 2.5 Integration
Connects your enhanced memory system to GPT-4 for live tutoring
"""

import openai
from typing import Dict, Any, List, Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for OpenAI API integration with enhanced memory"""
    
    def __init__(self):
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_model or "gpt-4"
    
    async def generate_socratic_response(
        self, 
        memory_context: str, 
        user_message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Generate Socratic tutoring response using 4-layer memory context
        """
        
        try:
            # Build messages with your memory context as system prompt
            messages = [
                {
                    "role": "system",
                    "content": memory_context  # Your brilliant 4-layer context
                }
            ]
            
            # Add conversation history if available
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 6 messages
            
            # Add current user message
            messages.append({
                "role": "user", 
                "content": user_message
            })
            
            # Generate response with GPT-4
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Balanced creativity for tutoring
                max_tokens=500,   # Socratic responses should be focused
                top_p=0.9
            )
            
            ai_response = response.choices[0].message.content
            
            # Analyze response for Socratic effectiveness
            socratic_analysis = await self._analyze_socratic_response(ai_response)
            
            return {
                "response": ai_response,
                "socratic_analysis": socratic_analysis,
                "token_usage": response.usage._asdict(),
                "model_used": self.model,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            return await self._create_fallback_response(user_message)
    
    async def _analyze_socratic_response(self, response: str) -> Dict[str, Any]:
        """Analyze if response follows Socratic methodology"""
        
        question_count = response.count('?')
        has_direct_answer = any(phrase in response.lower() for phrase in [
            'the answer is', 'it is', 'this means', 'the definition'
        ])
        
        return {
            "question_count": question_count,
            "socratic_compliance": "high" if question_count >= 2 and not has_direct_answer else "moderate",
            "engagement_level": "high" if question_count > 0 else "low",
            "teaching_approach": "questioning" if question_count >= 2 else "explanatory"
        }
    
    async def _create_fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Create fallback response when OpenAI fails"""
        
        fallback_responses = [
            "That's an interesting question! What experiences have you had that might relate to this?",
            "I'm curious about your thinking here. Can you tell me more about what sparked this question?",
            "Let's explore this together. What comes to mind when you think about this topic?"
        ]
        
        return {
            "response": fallback_responses[0],  # Could randomize
            "socratic_analysis": {"fallback": True, "socratic_compliance": "high"},
            "success": False,
            "error": "OpenAI service unavailable - using fallback"
        }
```

### Step 2: Enhanced Chat Endpoint 

**Update: `backend/app/api/v1/endpoints/chat.py`** (NEW FILE)
```python
"""
Enhanced Chat API - Phase 2.5 Implementation
Live AI tutoring with 4-layer memory integration
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Conversation, Message
from app.services.memory_service import EnhancedMemoryService
from app.services.openai_service import OpenAIService
from app.schemas.chat import (
    ChatRequest, ChatResponse, SocraticAnalysis, 
    ConversationCreateResponse
)

router = APIRouter()

@router.post("/{module_id}", response_model=ChatResponse)
async def chat_with_enhanced_memory(
    module_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    **Phase 2.5: Live AI Tutoring with Enhanced Memory**
