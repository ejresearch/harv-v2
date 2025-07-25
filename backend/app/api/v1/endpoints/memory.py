"""
Memory System API Endpoints - Phase 2 Integration
REST API for enhanced 4-layer memory system
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Conversation, Message
from app.services.memory_service import EnhancedMemoryService
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

# Pydantic schemas for memory API
class MemoryContextResponse(BaseModel):
    assembled_prompt: str
    context_size: int
    layers_active: int
    assembly_timestamp: str
    success: bool
    layer1_profile: Dict[str, Any]
    layer2_module: Dict[str, Any] 
    layer3_conversation: Dict[str, Any]
    layer4_connections: Dict[str, Any]
    error: Optional[str] = None

@router.get("/context/{module_id}", response_model=MemoryContextResponse)
async def get_memory_context(module_id: int, current_message: str = Query("", description="Current student message for context"), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get enhanced 4-layer memory context for AI chat"""
    try:
        memory_service = EnhancedMemoryService(db)
        context = await memory_service.assemble_memory_context(user_id=current_user.id, module_id=module_id, current_message=current_message)
        return MemoryContextResponse(**context)
    except Exception as e:
        logger.error(f"Memory context assembly failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to assemble memory context: {str(e)}")

@router.get("/health")
async def memory_system_health(db: Session = Depends(get_db)):
    """Health check for memory system"""
    try:
        user_count = db.query(User).count()
        memory_service = EnhancedMemoryService(db)
        return {"status": "healthy", "memory_service": "initialized", "database": "connected", "users_in_system": user_count, "layers_available": 4, "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        logger.error(f"Memory system health check failed: {str(e)}")
        return {"status": "unhealthy", "error": str(e), "timestamp": datetime.utcnow().isoformat()}

@router.post("/demo/{module_id}")
async def demo_memory_system(module_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Demo endpoint showing complete memory system flow"""
    try:
        memory_service = EnhancedMemoryService(db)
        test_message = "I'm having trouble understanding how nonverbal communication affects message interpretation. Can you help me explore this concept?"
        context = await memory_service.assemble_memory_context(user_id=current_user.id, module_id=module_id, current_message=test_message)
        
        return {
            "demo_message": test_message,
            "memory_context": context,
            "layers_breakdown": {
                "layer1_profile": f"Loaded user learning profile with {len(context['layer1_profile'].get('content', ''))} characters",
                "layer2_module": f"Loaded module {module_id} context with {len(context['layer2_module'].get('content', ''))} characters",
                "layer3_conversation": f"Loaded conversation state with {len(context['layer3_conversation'].get('content', ''))} characters",
                "layer4_connections": f"Loaded knowledge connections with {len(context['layer4_connections'].get('content', ''))} characters"
            },
            "system_performance": {"total_context_size": context["context_size"], "layers_active": context["layers_active"], "assembly_successful": context["success"]},
            "next_steps": ["Integrate with OpenAI API for AI responses", "Add real-time memory updates", "Implement learning analytics dashboard", "Connect to frontend chat interface"]
        }
    except Exception as e:
        logger.error(f"Memory system demo failed: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Demo failed: {str(e)}")
