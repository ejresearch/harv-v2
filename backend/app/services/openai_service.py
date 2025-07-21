"""
OpenAI Chat Service - Phase 2.5 Complete Integration
Connects your enhanced memory system to GPT-4 for live Socratic tutoring
"""

import logging
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    """Service for OpenAI API integration with enhanced memory"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
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
            logger.info(f"🤖 Generating response with {len(memory_context)} chars of memory context")
            
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
            
            logger.info(f"🤖 Sending to {self.model} with {len(messages)} messages")
            
            # Generate response with GPT-4
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,  # Balanced creativity for tutoring
                max_tokens=500,   # Socratic responses should be focused
                top_p=0.9
            )
            
            ai_response = response.choices[0].message.content
            
            # Analyze response for Socratic effectiveness
            socratic_analysis = await self._analyze_socratic_response(ai_response)
            
            logger.info(f"✅ Generated {len(ai_response)} char response with {socratic_analysis['question_count']} questions")
            
            return {
                "response": ai_response,
                "socratic_analysis": socratic_analysis,
                "token_usage": response.usage.model_dump() if response.usage else {},
                "model_used": self.model,
                "success": True,
                "memory_context_chars": len(memory_context)
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI generation failed: {e}")
            return await self._create_fallback_response(user_message)
    
    async def _analyze_socratic_response(self, response: str) -> Dict[str, Any]:
        """Analyze if response follows Socratic methodology"""
        
        question_count = response.count('?')
        has_direct_answer = any(phrase in response.lower() for phrase in [
            'the answer is', 'it is defined as', 'communication is', 'the definition'
        ])
        
        # Check for Socratic patterns
        socratic_words = ['what', 'how', 'why', 'can you think', 'have you noticed', 'consider']
        socratic_count = sum(1 for word in socratic_words if word in response.lower())
        
        return {
            "question_count": question_count,
            "socratic_compliance": "high" if question_count >= 2 and not has_direct_answer else "moderate" if question_count >= 1 else "low",
            "engagement_level": "high" if socratic_count >= 2 else "moderate" if socratic_count >= 1 else "low",
            "teaching_approach": "questioning" if question_count >= 2 else "mixed" if question_count >= 1 else "explanatory",
            "has_direct_answers": has_direct_answer,
            "socratic_word_count": socratic_count
        }
    
    async def _create_fallback_response(self, user_message: str) -> Dict[str, Any]:
        """Create fallback response when OpenAI fails"""
        
        # Intelligent fallbacks based on message content
        message_lower = user_message.lower()
        
        if 'communication' in message_lower:
            fallback = "That's a thought-provoking question about communication! Can you think of a recent conversation you had? What made it effective or challenging?"
        elif any(word in message_lower for word in ['what', 'how', 'why']):
            fallback = "I see you're asking an important question! Before I share thoughts, what's your initial thinking on this? What comes to mind first?"
        else:
            fallback = "That's an interesting perspective! What experiences have you had that relate to this topic?"
        
        return {
            "response": fallback,
            "socratic_analysis": {
                "question_count": 2,
                "socratic_compliance": "high", 
                "engagement_level": "high",
                "teaching_approach": "questioning",
                "fallback": True
            },
            "success": False,
            "error": "OpenAI service unavailable - using intelligent fallback",
            "model_used": "fallback_socratic"
        }
