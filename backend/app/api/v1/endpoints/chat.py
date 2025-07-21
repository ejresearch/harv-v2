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
    
    Your memory system + OpenAI GPT-4 = Intelligent Socratic Tutor
    """
    
    try:
        # Initialize services
        memory_service = EnhancedMemoryService(db)
        openai_service = OpenAIService()
        
        # Get or create conversation
        conversation = await _get_or_create_conversation(
            db, current_user.id, module_id, request.conversation_id
        )
        
        # Assemble your brilliant 4-layer memory context
        memory_context = await memory_service.assemble_enhanced_context(
            user_id=current_user.id,
            module_id=module_id,
            current_message=request.message,
            conversation_id=str(conversation.id)
        )
        
        # Get conversation history for context
        conversation_history = await _get_conversation_history(db, conversation.id)
        
        # Generate Socratic response using memory + OpenAI
        ai_response = await openai_service.generate_socratic_response(
            memory_context=memory_context['assembled_prompt'],
            user_message=request.message,
            conversation_history=conversation_history
        )
        
        # Save conversation messages
        await _save_conversation_messages(
            db, conversation.id, request.message, 
            ai_response['response'], memory_context
        )
        
        # Update learning progress
        await _update_learning_progress(
            db, memory_service, current_user.id, module_id,
            ai_response['socratic_analysis']
        )
        
        return ChatResponse(
            message=ai_response['response'],
            conversation_id=str(conversation.id),
            module_id=module_id,
            enhanced_memory_used=True,
            memory_metrics={
                "context_chars": memory_context['context_metrics']['total_chars'],
                "layers_active": len([k for k, v in memory_context['database_status'].items() if v]),
                "optimization_score": memory_context['context_metrics']['optimization_score']
            },
            socratic_analysis=SocraticAnalysis(**ai_response['socratic_analysis']),
            model_info={
                "model": ai_response.get('model_used', 'gpt-4'),
                "tokens": ai_response.get('token_usage', {}),
                "success": ai_response['success']
            }
        )
        
    except Exception as e:
        logger.error(f"Enhanced chat error: {e}")
        # Fallback to memory-only response
        return await _create_memory_fallback_response(
            memory_service, current_user.id, module_id, request.message
        )

@router.post("/conversations", response_model=ConversationCreateResponse)
async def create_new_conversation(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start a new tutoring conversation for a module"""
    
    conversation = Conversation(
        user_id=current_user.id,
        module_id=module_id,
        title=f"Learning Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        is_active=True
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return ConversationCreateResponse(
        conversation_id=str(conversation.id),
        module_id=module_id,
        title=conversation.title,
        created_at=conversation.created_at.isoformat()
    )

# Helper functions for clean code organization
async def _get_or_create_conversation(db: Session, user_id: int, module_id: int, conversation_id: str = None):
    """Get existing conversation or create new one"""
    # Implementation details...

async def _get_conversation_history(db: Session, conversation_id: int):
    """Get recent conversation messages for context"""
    # Implementation details...

async def _save_conversation_messages(db: Session, conversation_id: int, user_msg: str, ai_msg: str, memory_context: dict):
    """Save both user and AI messages"""
    # Implementation details...

async def _update_l
