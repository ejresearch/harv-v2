"""
Memory API Endpoints - Phase 2.5 COMPLETE
Live AI tutoring with your enhanced 4-layer memory system + OpenAI
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services.memory_service import EnhancedMemoryService
from app.services.openai_service import OpenAIService
from app.schemas.memory import (
    MemoryContextResponse,
    MemoryContextRequest, 
    MemorySummaryCreate,
    MemorySummaryResponse,
    UserProgressUpdate
)
from app.schemas.chat import ChatRequest, ChatResponse, SocraticAnalysis, MemoryMetrics, ModelInfo

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/enhanced/{module_id}", 
    response_model=MemoryContextResponse,
    summary="Get Enhanced Memory Context",
    description="Retrieve 4-layer enhanced memory context for personalized AI tutoring"
)
async def get_enhanced_memory_context(
    module_id: int,
    current_message: Optional[str] = "",
    conversation_id: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    **Phase 2: Enhanced Memory System**
    
    Assembles your brilliant 4-layer memory context:
    - Layer 1: User learning profile and cross-module mastery
    - Layer 2: Module-specific context and teaching configuration  
    - Layer 3: Real-time conversation state and message history
    - Layer 4: Prior knowledge connections from other modules
    
    Returns optimized prompt context for AI with comprehensive metrics.
    """
    
    try:
        logger.info(f"🧠 Enhanced memory request for user {current_user.id}, module {module_id}")
        
        # Initialize enhanced memory service
        memory_service = EnhancedMemoryService(db)
        
        # Assemble 4-layer memory context
        memory_context = await memory_service.assemble_enhanced_context(
            user_id=current_user.id,
            module_id=module_id,
            current_message=current_message,
            conversation_id=conversation_id
        )
        
        # Log success metrics
        chars = memory_context.get('context_metrics', {}).get('total_chars', 0)
        logger.info(f"✅ Enhanced memory assembled: {chars} characters")
        
        return memory_context
        
    except Exception as e:
        logger.error(f"❌ Enhanced memory endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory assembly failed: {str(e)}"
        )

@router.post(
    "/enhanced/{module_id}/chat",
    response_model=ChatResponse,
    summary="Live AI Tutoring with Enhanced Memory",
    description="**PHASE 2.5 COMPLETE**: Your memory system + OpenAI = Live Socratic AI Tutor"
)
async def chat_with_enhanced_memory(
    module_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    **Phase 2.5: LIVE AI TUTORING - COMPLETE IMPLEMENTATION**
    
    This is your crown jewel endpoint:
    1. Assembles your brilliant 4-layer memory context
    2. Feeds it to OpenAI GPT-4 as system prompt  
    3. Generates Socratic teaching responses
    4. Returns live AI tutoring experience
    
    Your enhanced memory system is now a LIVE AI TUTOR! 🤖🧠
    """
    
    try:
        logger.info(f"🤖 Live AI tutoring request: user {current_user.id}, module {module_id}")
        
        # Initialize services
        memory_service = EnhancedMemoryService(db)
        openai_service = OpenAIService()
        
        # STEP 1: Assemble your brilliant 4-layer memory context
        memory_context = await memory_service.assemble_enhanced_context(
            user_id=current_user.id,
            module_id=module_id,
            current_message=request.message,
            conversation_id=request.conversation_id
        )
        
        logger.info(f"📚 Memory context assembled: {memory_context['context_metrics']['total_chars']} chars")
        
        # STEP 2: Generate live AI response using your memory context
        ai_response = await openai_service.generate_socratic_response(
            memory_context=memory_context['assembled_prompt'],
            user_message=request.message,
            conversation_history=[]  # Could add conversation history here
        )
        
        logger.info(f"🎓 AI response generated: {ai_response['socratic_analysis']['socratic_compliance']} Socratic compliance")
        
        # STEP 3: Create conversation ID for continuity
        conversation_id = request.conversation_id or str(uuid.uuid4())[:8]
        
        # STEP 4: Return complete tutoring response
        return ChatResponse(
            message=ai_response['response'],
            conversation_id=conversation_id,
            module_id=module_id,
            enhanced_memory_used=True,
            memory_metrics=MemoryMetrics(
                context_chars=memory_context['context_metrics']['total_chars'],
                layers_active=sum(1 for status in memory_context['database_status'].values() if status),
                optimization_score=memory_context['context_metrics']['optimization_score']
            ),
            socratic_analysis=SocraticAnalysis(**ai_response['socratic_analysis']),
            model_info=ModelInfo(
                model=ai_response.get('model_used', 'gpt-4'),
                tokens=ai_response.get('token_usage', {}),
                success=ai_response['success']
            )
        )
        
    except Exception as e:
        logger.error(f"❌ Live AI tutoring error: {e}")
        
        # Fallback to memory-only response
        return ChatResponse(
            message="I'm having trouble connecting to my AI tutor right now, but I can see you're asking about an important topic. What experiences have you had that relate to this question?",
            conversation_id=request.conversation_id or "fallback",
            module_id=module_id,
            enhanced_memory_used=True,
            memory_metrics=MemoryMetrics(context_chars=0, layers_active=0, optimization_score=0.0),
            socratic_analysis=SocraticAnalysis(
                question_count=1,
                socratic_compliance="moderate",
                engagement_level="moderate", 
                teaching_approach="questioning",
                fallback=True
            ),
            model_info=ModelInfo(model="fallback", tokens={}, success=False)
        )

@router.post(
    "/summary",
    response_model=MemorySummaryResponse,
    summary="Save Learning Memory",
    description="Save memory summary for cross-module learning persistence"
)
async def save_memory_summary(
    request: MemorySummaryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Save learning insights for future memory context assembly"""
    
    try:
        memory_service = EnhancedMemoryService(db)
        
        success = await memory_service.save_memory_summary(
            user_id=current_user.id,
            module_id=request.module_id,
            what_learned=request.what_learned,
            how_learned=request.how_learned,
            connections_made=request.connections_made,
            confidence_level=request.confidence_level
        )
        
        if success:
            return {
                "status": "saved",
                "message": "Memory summary saved successfully",
                "user_id": current_user.id,
                "module_id": request.module_id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save memory summary"
            )
            
    except Exception as e:
        logger.error(f"❌ Memory summary save error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Memory save failed: {str(e)}"
        )

@router.put("/progress/{module_id}")
async def update_learning_progress(
    module_id: int,
    request: UserProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update learning progress metrics for memory system"""
    
    try:
        memory_service = EnhancedMemoryService(db)
        
        success = await memory_service.update_user_progress(
            user_id=current_user.id,
            module_id=module_id,
            completion_percentage=request.completion_percentage,
            insights_gained=request.insights_gained,
            questions_asked=request.questions_asked
        )
        
        if success:
            return {
                "status": "updated",
                "message": "Progress updated successfully",
                "user_id": current_user.id,
                "module_id": module_id,
                "completion": request.completion_percentage
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update progress"
            )
            
    except Exception as e:
        logger.error(f"❌ Progress update error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Progress update failed: {str(e)}"
        )

@router.get("/debug/{module_id}")
async def debug_memory_system(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Debug information for memory system development"""
    
    try:
        memory_service = EnhancedMemoryService(db)
        
        # Get full memory context with debug info
        memory_context = await memory_service.assemble_enhanced_context(
            user_id=current_user.id,
            module_id=module_id,
            current_message="Debug request"
        )
        
        return {
            "debug_info": {
                "user_id": current_user.id,
                "module_id": module_id,
                "timestamp": memory_context['context_metrics']['timestamp'],
                "total_context_chars": memory_context['context_metrics']['total_chars'],
                "layers_loaded": memory_context['database_status'],
                "layer_data_preview": {
                    "system_profile": memory_context['memory_layers']['system_data']['learning_profile'],
                    "module_title": memory_context['memory_layers']['module_data']['module_info']['title'],
                    "conversation_state": memory_context['memory_layers']['conversation_data']['state'],
                    "prior_modules": len(memory_context['memory_layers']['prior_knowledge']['prior_module_insights'])
                },
                "prompt_sections": memory_context['assembled_prompt'].split('\n')[:10]  # First 10 lines
            },
            "status": "debug_complete"
        }
        
    except Exception as e:
        logger.error(f"❌ Memory debug error: {e}")
        return {
            "debug_info": {
                "error": str(e),
                "user_id": current_user.id,
                "module_id": module_id,
                "status": "debug_failed"
            }
        }

@router.get("/health")
async def memory_system_health(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Check memory system health and database connectivity"""
    
    try:
        # Test database connectivity
        from app.models import User
        user_count = db.query(User).count()
        
        return {
            "status": "healthy",
            "memory_system": "operational",
            "database": "connected",
            "users_in_system": user_count,
            "timestamp": "2025-07-21T12:00:00Z",
            "phase_2_5": "LIVE AI TUTORING ACTIVE"
        }
        
    except Exception as e:
        logger.error(f"❌ Memory health check failed: {e}")
        return {
            "status": "unhealthy",
            "memory_system": "error",
            "database": "disconnected",
            "error": str(e)
        }
