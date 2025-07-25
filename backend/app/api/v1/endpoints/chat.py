"""
Enhanced Chat API - Phase 2.5: Memory + GPT-4o Integration
Connects your brilliant 4-layer memory system to GPT-4o for real AI tutoring
NO FAKE RESPONSES - Uses actual GPT-4o API with enhanced memory context
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import json
import logging

from app.core.database import get_db
from app.core.security import get_current_user_optional, get_current_user
from app.models.user import User
from app.services.openai_service import OpenAIService, SocraticAnalysis
from app.services.memory_service import EnhancedMemoryService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
openai_service = OpenAIService()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="Student's question or message")
    module_id: int = Field(..., ge=1, le=15, description="Current module (1-15)")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for continuity")
    user_id: Optional[int] = Field(None, description="User ID (for development/testing)")
    conversation_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous messages")
    socratic_mode: bool = Field(True, description="Enable Socratic teaching methodology")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI tutor's response")
    conversation_id: str = Field(..., description="Unique conversation identifier")
    module_id: int = Field(..., description="Current module")
    memory_metrics: Dict[str, Any] = Field(..., description="Memory system performance metrics")
    socratic_analysis: SocraticAnalysis = Field(..., description="Socratic methodology analysis")
    token_usage: Dict[str, Any] = Field(..., description="OpenAI token usage and cost")
    model_used: str = Field(..., description="AI model used for response")
    enhanced: bool = Field(True, description="Enhanced memory system active")
    timestamp: str = Field(..., description="Response timestamp")
    success: bool = Field(..., description="Request success status")
    learning_insights: Optional[Dict[str, Any]] = Field(None, description="Learning analytics data")

@router.post("/enhanced", response_model=ChatResponse)
async def chat_enhanced_with_openai(
    request: ChatRequest, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Enhanced chat with REAL GPT-4o integration + 4-layer memory system
    
    This is the crown jewel endpoint that combines:
    - Your brilliant 4-layer enhanced memory system
    - Real GPT-4o API integration (most advanced AI model)
    - Socratic methodology enforcement
    - Real-time learning analytics
    
    Flow:
    1. Assemble enhanced memory context (4 layers)
    2. Send context + message to GPT-4o
    3. Analyze response for Socratic compliance
    4. Update memory with conversation insights
    5. Return comprehensive response with analytics
    """
    
    try:
        logger.info(f"🚀 Enhanced chat request - Module: {request.module_id}, User: {current_user.id if current_user else 'anonymous'}")
        
        # Generate conversation ID if not provided
        conv_id = request.conversation_id or str(uuid.uuid4())
        
        # Determine user ID (from auth or request for testing)
        user_id = current_user.id if current_user else request.user_id
        if not user_id:
            raise HTTPException(status_code=400, detail="User authentication required or user_id must be provided")
        
        # Initialize enhanced memory service
        memory_service = EnhancedMemoryService(db)
        
        # Step 1: Assemble enhanced memory context using your 4-layer system
        logger.info("🧠 Assembling enhanced memory context...")
        try:
            memory_context_result = await memory_service.assemble_memory_context(
                user_id=user_id,
                module_id=request.module_id,
                current_message=request.message,
                conversation_id=conv_id
            )
            
            if not memory_context_result["success"]:
                logger.warning(f"⚠️ Memory assembly failed: {memory_context_result.get('error', 'Unknown error')}")
                # Continue with fallback context instead of failing
                enhanced_memory_context = f"Student is learning Module {request.module_id}. Current message: {request.message}"
                memory_metrics = {"layers_active": 0, "success": False}
            else:
                enhanced_memory_context = memory_context_result["assembled_prompt"]
                memory_metrics = memory_context_result.get("metrics", {})
                logger.info(f"✅ Memory context assembled: {len(enhanced_memory_context)} characters")
        
        except Exception as e:
            logger.warning(f"⚠️ Memory service error: {e}")
            enhanced_memory_context = f"Student is learning Module {request.module_id}. Current message: {request.message}"
            memory_metrics = {"layers_active": 0, "success": False, "error": str(e)}
        
        # Step 2: Generate AI response using GPT-4o + memory context
        logger.info("🤖 Calling GPT-4o with enhanced memory context...")
        openai_response = await openai_service.generate_socratic_response(
            enhanced_memory_context=enhanced_memory_context,
            user_message=request.message,
            conversation_history=request.conversation_history or [],
            module_id=request.module_id
        )
        
        if not openai_response.success:
            raise HTTPException(
                status_code=500, 
                detail=f"GPT-4o API error: {openai_response.error}"
            )
        
        # Step 3: Extract response components
        ai_reply = openai_response.response
        socratic_analysis = openai_response.socratic_analysis
        token_usage = openai_response.token_usage
        
        logger.info(f"✅ GPT-4o response: {len(ai_reply)} characters")
        logger.info(f"📊 Socratic compliance: {socratic_analysis.socratic_compliance}")
        logger.info(f"💰 Token usage: {token_usage.total_tokens} tokens (${token_usage.estimated_cost:.4f})")
        
        # Step 4: Generate learning insights
        learning_insights = await _generate_learning_insights(
            user_message=request.message,
            ai_response=ai_reply,
            socratic_analysis=socratic_analysis,
            memory_metrics=memory_metrics,
            module_id=request.module_id
        )
        
        # Step 5: Update memory with conversation insights (async)
        try:
            if hasattr(memory_service, 'save_conversation_insights'):
                await memory_service.save_conversation_insights(
                    user_id=user_id,
                    module_id=request.module_id,
                    conversation_id=conv_id,
                    user_message=request.message,
                    ai_response=ai_reply,
                    socratic_score=socratic_analysis.effectiveness_score,
                    key_insights=learning_insights.get("key_concepts", []),
                    learning_connections=learning_insights.get("cross_module_connections", [])
                )
                logger.info("💾 Conversation insights saved to memory")
        except Exception as e:
            logger.warning(f"⚠️ Failed to save insights: {e}")
            # Don't fail the request for memory save issues
        
        # Step 6: Build comprehensive response
        return ChatResponse(
            reply=ai_reply,
            conversation_id=conv_id,
            module_id=request.module_id,
            memory_metrics=memory_metrics,
            socratic_analysis=socratic_analysis,
            token_usage=token_usage.dict(),
            model_used=token_usage.model_used,
            enhanced=True,
            timestamp=datetime.now().isoformat(),
            success=True,
            learning_insights=learning_insights
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Enhanced chat error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Enhanced chat service error: {str(e)}"
        )

@router.get("/openai/status")
async def get_openai_status():
    """Get GPT-4o service status and metrics"""
    
    try:
        # Test OpenAI connection
        connection_status = await openai_service.test_connection()
        
        # Get service metrics
        metrics = openai_service.get_service_metrics()
        
        return {
            "status": "operational",
            "model": "gpt-4o",
            "connection": connection_status,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ GPT-4o status check error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.post("/demo/{module_id}")
async def demo_enhanced_chat(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Demo the complete enhanced chat system with GPT-4o
    Perfect for testing memory + GPT-4o integration
    """
    
    demo_messages = [
        "Hi, I'm struggling to understand effective communication techniques.",
        "What makes communication successful in professional settings?", 
        "How do nonverbal cues affect the message being communicated?"
    ]
    
    results = []
    conversation_id = str(uuid.uuid4())
    
    for i, message in enumerate(demo_messages):
        logger.info(f"🎭 Demo message {i+1}: {message}")
        
        # Create demo request
        demo_request = ChatRequest(
            message=message,
            module_id=module_id,
            conversation_id=conversation_id,
            user_id=current_user.id if current_user else 1  # Demo user
        )
        
        # Process through enhanced chat
        try:
            response = await chat_enhanced_with_openai(demo_request, db, current_user)
            
            results.append({
                "user_message": message,
                "ai_response": response.reply,
                "socratic_score": response.socratic_analysis.effectiveness_score,
                "question_count": response.socratic_analysis.question_count,
                "token_usage": response.token_usage["total_tokens"],
                "memory_layers_active": response.memory_metrics.get("layers_active", 0),
                "cost": response.token_usage.get("estimated_cost", 0)
            })
            
        except Exception as e:
            results.append({
                "user_message": message,
                "error": str(e)
            })
    
    return {
        "demo_complete": True,
        "conversation_id": conversation_id,
        "module_id": module_id,
        "total_exchanges": len(demo_messages),
        "results": results,
        "system_status": {
            "enhanced_memory": "active",
            "gpt4o_integration": "active",
            "socratic_methodology": "enforced"
        },
        "timestamp": datetime.now().isoformat()
    }

# Helper functions

async def _generate_learning_insights(
    user_message: str,
    ai_response: str,
    socratic_analysis: SocraticAnalysis,
    memory_metrics: Dict[str, Any],
    module_id: int
) -> Dict[str, Any]:
    """Generate learning insights from conversation"""
    
    insights = {
        "key_concepts": [],
        "learning_level": "intermediate",
        "engagement_score": socratic_analysis.effectiveness_score,
        "cross_module_connections": [],
        "recommended_follow_up": []
    }
    
    # Extract key concepts from user message
    if "communication" in user_message.lower():
        insights["key_concepts"].append("Communication fundamentals")
    if "nonverbal" in user_message.lower():
        insights["key_concepts"].append("Nonverbal communication")
    if "professional" in user_message.lower():
        insights["key_concepts"].append("Professional communication")
    
    # Determine learning level based on question complexity
    if len(user_message.split()) > 15:
        insights["learning_level"] = "advanced"
    elif len(user_message.split()) < 8:
        insights["learning_level"] = "beginner"
    
    # Generate cross-module connections
    if module_id == 1:  # Communication module
        insights["cross_module_connections"] = [
            "Module 2: Verbal communication skills",
            "Module 3: Active listening techniques"
        ]
    
    # Recommend follow-up questions
    if socratic_analysis.question_count >= 2:
        insights["recommended_follow_up"] = [
            "Explore specific examples from your experience",
            "Consider how this applies in different contexts"
        ]
    
    return insights
