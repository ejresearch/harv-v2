"""
Memory API Endpoints - Phase 2 Integration
Exposes your enhanced 4-layer memory system through clean REST API

File: backend/app/api/v1/endpoints/memory.py
"""

from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User
from app.services.memory_service import EnhancedMemoryService
from app.schemas.memory import (
    MemoryContextResponse,
    MemoryContextRequest, 
    MemorySummaryCreate,
    MemorySummaryResponse,
    UserProgressUpdate
)

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
    summary="Chat with Enhanced Memory",
    description="Send message to AI tutor with full 4-layer memory context"
)
async def chat_with_enhanced_memory(
    module_id: int,
    request: MemoryContextRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    **Phase 2: Enhanced Chat Integration**
    
    Sends message to AI tutor with full memory context assembly.
    Integrates your Socratic methodology with 4-layer memory system.
    """
    
    try:
        # Initialize services
        memory_service = EnhancedMemoryService(db)
        
        # Assemble memory context for this message
        memory_context = await memory_service.assemble_enhanced_context(
            user_id=current_user.id,
            module_id=module_id,
            current_message=request.message,
            conversation_id=request.conversation_id
        )
        
        # TODO: Phase 2.5 - Integrate with OpenAI API
        # For now, return the memory context to validate the system
        return {
            "status": "memory_assembled",
            "message": request.message,
            "memory_context_chars": memory_context['context_metrics']['total_chars'],
            "memory_layers_active": len([k for k, v in memory_context['database_status'].items() if v]),
            "assembled_prompt_preview": memory_context['assembled_prompt'][:200] + "...",
            "next_phase": "OpenAI integration with enhanced memory context"
        }
        
    except Exception as e:
        logger.error(f"❌ Enhanced chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enhanced chat failed: {str(e)}"
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
    """
    **Memory Persistence**
    
    Saves learning insights for future memory context assembly.
    Critical for cross-module learning connections.
    """
    
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

@router.put(
    "/progress/{module_id}",
    summary="Update User Progress",
    description="Update learning progress metrics for memory system"
)
async def update_learning_progress(
    module_id: int,
    request: UserProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    **Progress Tracking**
    
    Updates user progress metrics used by the memory system
    for personalized learning optimization.
    """
    
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

@router.get(
    "/debug/{module_id}",
    summary="Debug Memory System",
    description="Debug information for memory system development"
)
async def debug_memory_system(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    **Development Debug Endpoint**
    
    Provides detailed debugging information for memory system development.
    Shows exactly what data is being loaded from each layer.
    """
    
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

# Health check for memory system
@router.get(
    "/health",
    summary="Memory System Health",
    description="Health check for enhanced memory system"
)
async def memory_system_health(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Check memory system health and database connectivity"""
    
    try:
        # Test database connectivity
        user_count = db.query(User).count()
        
        return {
            "status": "healthy",
            "memory_system": "operational",
            "database": "connected",
            "users_in_system": user_count,
            "timestamp": "2025-07-21T12:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"❌ Memory health check failed: {e}")
        return {
            "status": "unhealthy",
            "memory_system": "error",
            "database": "disconnected",
            "error": str(e)
        }
