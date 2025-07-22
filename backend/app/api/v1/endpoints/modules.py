# backend/app/api/v1/endpoints/modules.py
"""
Production Modules API - Real Database Integration
Builds on your existing Module model and authentication system
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.course import Module
from app.models.conversation import Conversation, Message, UserProgress
from app.models.memory import MemorySummary

router = APIRouter()

# =========================================================================
# PYDANTIC SCHEMAS (Using your existing models)
# =========================================================================

class UserProgressData(BaseModel):
    completion_percentage: float
    conversations_count: int
    messages_count: int
    mastery_level: str
    time_spent_minutes: int
    last_accessed: Optional[str] = None
    memory_summaries_count: int
    objectives_completed: List[str]
    recent_activity: List[dict]

class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    learning_objectives: List[str]
    difficulty_level: str
    estimated_duration: int
    system_prompt: str
    module_prompt: str
    resources: Optional[str] = None
    user_progress: UserProgressData
    created_at: str
    updated_at: str

class ModuleListItem(BaseModel):
    id: int
    title: str
    description: str
    difficulty_level: str
    estimated_duration: int
    completion_percentage: float
    conversations_count: int
    is_available: bool
    
class ModuleStatsResponse(BaseModel):
    module_id: int
    title: str
    total_users: int
    total_conversations: int
    total_messages: int
    average_completion: float
    average_session_duration: float
    popular_topics: List[dict]
    recent_activity: List[dict]

# =========================================================================
# HELPER FUNCTIONS - Real Database Calculations
# =========================================================================

def calculate_real_progress(db: Session, user_id: int, module_id: int) -> UserProgressData:
    """Calculate REAL user progress from actual database data"""
    
    # Get all conversations for this user/module
    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id,
        Conversation.module_id == module_id
    ).options(joinedload(Conversation.messages)).all()
    
    # Calculate real metrics
    total_conversations = len(conversations)
    total_messages = sum(len(conv.messages) for conv in conversations)
    
    # Calculate time spent from conversation timestamps
    total_time_minutes = 0
    for conv in conversations:
        if conv.messages and len(conv.messages) > 1:
            start_time = min(msg.created_at for msg in conv.messages)
            end_time = max(msg.created_at for msg in conv.messages)
            session_duration = (end_time - start_time).total_seconds() / 60
            # Minimum 5 minutes per conversation, cap at 120 minutes
            total_time_minutes += max(min(session_duration, 120), 5)
    
    # Get memory summaries for this module
    memory_summaries = db.query(MemorySummary).filter(
        MemorySummary.user_id == user_id,
        MemorySummary.module_id == module_id
    ).all()
    
    memory_count = len(memory_summaries)
    
    # Calculate objectives completion based on engagement patterns
    objectives_completed = []
    
    # Basic engagement thresholds
    if total_conversations >= 1:
        objectives_completed.append("Started learning conversation")
    
    if total_messages >= 10:
        objectives_completed.append("Active participation in dialogue")
        
    if memory_count >= 1:
        objectives_completed.append("Generated learning insights")
        
    if total_messages >= 20:
        objectives_completed.append("Sustained engagement with content")
        
    if memory_count >= 2:
        objectives_completed.append("Made cross-concept connections")
        
    if total_time_minutes >= 30:
        objectives_completed.append("Deep exploration of topics")
    
    # Calculate completion percentage based on multiple factors
    completion_factors = {
        'conversations': min(total_conversations * 20, 30),  # Up to 30% for conversations
        'messages': min(total_messages * 2, 25),            # Up to 25% for messages  
        'memory': min(memory_count * 15, 30),               # Up to 30% for memory summaries
        'time': min(total_time_minutes / 2, 15)             # Up to 15% for time spent
    }
    
    completion_percentage = min(sum(completion_factors.values()), 100.0)
    
    # Determine mastery level
    if completion_percentage >= 80:
        mastery_level = "advanced"
    elif completion_percentage >= 50:
        mastery_level = "intermediate" 
    elif completion_percentage >= 20:
        mastery_level = "beginner"
    else:
        mastery_level = "novice"
    
    # Get recent activity
    recent_conversations = conversations[-3:] if conversations else []
    recent_activity = []
    
    for conv in recent_conversations:
        if conv.messages:
            recent_activity.append({
                "conversation_id": conv.id,
                "title": conv.title or f"Session {conv.id}",
                "message_count": len(conv.messages),
                "last_activity": conv.updated_at.isoformat(),
                "summary": conv.summary[:100] + "..." if conv.summary else "Learning session"
            })
    
    last_accessed = None
    if conversations:
        last_conv = max(conversations, key=lambda c: c.updated_at)
        last_accessed = last_conv.updated_at.isoformat()
    
    return UserProgressData(
        completion_percentage=round(completion_percentage, 1),
        conversations_count=total_conversations,
        messages_count=total_messages,
        mastery_level=mastery_level,
        time_spent_minutes=int(total_time_minutes),
        last_accessed=last_accessed,
        memory_summaries_count=memory_count,
        objectives_completed=objectives_completed,
        recent_activity=recent_activity
    )

def get_module_stats(db: Session, module_id: int) -> ModuleStatsResponse:
    """Get real usage statistics for a module"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Count unique users who engaged with this module
    total_users = db.query(func.count(func.distinct(Conversation.user_id))).filter(
        Conversation.module_id == module_id
    ).scalar() or 0
    
    # Count total conversations
    total_conversations = db.query(func.count(Conversation.id)).filter(
        Conversation.module_id == module_id
    ).scalar() or 0
    
    # Count total messages
    total_messages = db.query(func.count(Message.id)).join(Conversation).filter(
        Conversation.module_id == module_id
    ).scalar() or 0
    
    # Calculate average completion percentage
    user_progresses = db.query(UserProgress.completion_percentage).filter(
        UserProgress.module_id == module_id
    ).all()
    
    if user_progresses:
        average_completion = sum(p[0] for p in user_progresses) / len(user_progresses)
    else:
        average_completion = 0.0
    
    # Calculate average session duration
    conversations_with_duration = db.query(Conversation).filter(
        Conversation.module_id == module_id
    ).options(joinedload(Conversation.messages)).all()
    
    session_durations = []
    for conv in conversations_with_duration:
        if conv.messages and len(conv.messages) > 1:
            start_time = min(msg.created_at for msg in conv.messages)
            end_time = max(msg.created_at for msg in conv.messages)
            duration = (end_time - start_time).total_seconds() / 60
            session_durations.append(max(duration, 5))  # Minimum 5 minutes
    
    average_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
    
    # Get recent activity (last 5 conversations)
    recent_conversations = db.query(Conversation).filter(
        Conversation.module_id == module_id
    ).order_by(desc(Conversation.updated_at)).limit(5).all()
    
    recent_activity = []
    for conv in recent_conversations:
        user = db.query(User).filter(User.id == conv.user_id).first()
        recent_activity.append({
            "conversation_id": conv.id,
            "user_name": user.name if user else "Unknown",
            "title": conv.title or f"Session {conv.id}",
            "message_count": len(conv.messages),
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat()
        })
    
    return ModuleStatsResponse(
        module_id=module_id,
        title=module.title,
        total_users=total_users,
        total_conversations=total_conversations,
        total_messages=total_messages,
        average_completion=round(average_completion, 1),
        average_session_duration=round(average_session_duration, 1),
        popular_topics=[],  # TODO: Implement topic analysis
        recent_activity=recent_activity
    )

# =========================================================================
# API ENDPOINTS - Production Ready
# =========================================================================

@router.get("/", response_model=List[ModuleListItem])
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    include_inactive: bool = Query(False, description="Include inactive modules")
):
    """
    Get all modules with REAL user progress data
    Returns modules with actual completion percentages calculated from database
    """
    
    # Get modules with optional inactive filter
    query = db.query(Module)
    if not include_inactive:
        query = query.filter(Module.is_active == True)
    
    modules = query.order_by(Module.id).all()
    
    result = []
    for module in modules:
        # Calculate real progress for this user
        progress_data = calculate_real_progress(db, current_user.id, module.id)
        
        # Check availability (could add prerequisites logic here)
        is_available = True
        
        result.append(ModuleListItem(
            id=module.id,
            title=module.title,
            description=module.description,
            difficulty_level=module.difficulty_level or "intermediate",
            estimated_duration=module.estimated_duration or 45,
            completion_percentage=progress_data.completion_percentage,
            conversations_count=progress_data.conversations_count,
            is_available=is_available
        ))
    
    return result

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module_details(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed module information with REAL progress data
    All progress calculations use actual database queries - no fake data
    """
    
    # Get module
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Calculate real user progress
    user_progress = calculate_real_progress(db, current_user.id, module_id)
    
    # Parse learning objectives
    try:
        learning_objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
    except (json.JSONDecodeError, TypeError):
        learning_objectives = []
    
    return ModuleResponse(
        id=module.id,
        title=module.title,
        description=module.description,
        learning_objectives=learning_objectives,
        difficulty_level=module.difficulty_level or "intermediate",
        estimated_duration=module.estimated_duration or 45,
        system_prompt=module.system_prompt or "",
        module_prompt=module.module_prompt or "",
        resources=module.resources,
        user_progress=user_progress,
        created_at=module.created_at.isoformat(),
        updated_at=module.updated_at.isoformat()
    )

@router.get("/{module_id}/stats", response_model=ModuleStatsResponse)
async def get_module_statistics(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get real usage statistics for a module
    Shows actual user engagement, completion rates, session durations
    """
    
    return get_module_stats(db, module_id)

@router.get("/{module_id}/config")
async def get_module_config(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get module configuration for memory system integration
    Returns prompts and settings for enhanced memory system
    """
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Parse learning objectives
    try:
        learning_objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
    except (json.JSONDecodeError, TypeError):
        learning_objectives = []
    
    return {
        "module_id": module.id,
        "title": module.title,
        "system_prompt": module.system_prompt,
        "module_prompt": module.module_prompt,
        "learning_objectives": learning_objectives,
        "teaching_config": {
            "socratic_mode": True,
            "prevent_direct_answers": True,
            "encourage_discovery": True,
            "difficulty_level": module.difficulty_level,
            "estimated_duration": module.estimated_duration
        },
        "memory_integration": {
            "use_enhanced_memory": True,
            "memory_layers": ["system_data", "module_data", "conversation_data", "prior_knowledge"],
            "context_window": 4000,
            "fallback_enabled": True
        }
    }

# =========================================================================
# MODULE MANAGEMENT (For future admin interface)
# =========================================================================

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    module_prompt: Optional[str] = None
    learning_objectives: Optional[List[str]] = None
    difficulty_level: Optional[str] = None
    estimated_duration: Optional[int] = None
    resources: Optional[str] = None
    is_active: Optional[bool] = None

@router.put("/{module_id}/config")
async def update_module_config(
    module_id: int,
    update_data: ModuleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update module configuration
    Future: Add admin role checking
    """
    
    # TODO: Add admin role verification
    # if not current_user.is_admin:
    #     raise HTTPException(status_code=403, detail="Admin access required")
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Update provided fields
    update_dict = update_data.dict(exclude_unset=True)
    
    # Handle learning objectives serialization
    if 'learning_objectives' in update_dict:
        update_dict['learning_objectives'] = json.dumps(update_dict['learning_objectives'])
    
    for field, value in update_dict.items():
        setattr(module, field, value)
    
    # Update timestamp
    module.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(module)
    
    return {
        "status": "updated",
        "module_id": module_id,
        "updated_fields": list(update_dict.keys()),
        "updated_at": module.updated_at.isoformat()
    }

# =========================================================================
# PERFORMANCE & DEBUG ENDPOINTS
# =========================================================================

@router.get("/{module_id}/debug/progress")
async def debug_progress_calculation(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Debug endpoint to show detailed progress calculation breakdown
    Shows how real database data is used to calculate completion percentages
    """
    
    # Get raw data
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.module_id == module_id
    ).options(joinedload(Conversation.messages)).all()
    
    memory_summaries = db.query(MemorySummary).filter(
        MemorySummary.user_id == current_user.id,
        MemorySummary.module_id == module_id
    ).all()
    
    # Calculate breakdown
    total_conversations = len(conversations)
    total_messages = sum(len(conv.messages) for conv in conversations)
    memory_count = len(memory_summaries)
    
    # Time calculation details
    time_breakdown = []
    total_time = 0
    
    for conv in conversations:
        if conv.messages and len(conv.messages) > 1:
            start_time = min(msg.created_at for msg in conv.messages)
            end_time = max(msg.created_at for msg in conv.messages)
            duration = (end_time - start_time).total_seconds() / 60
            duration = max(min(duration, 120), 5)  # Cap between 5-120 minutes
            total_time += duration
            
            time_breakdown.append({
                "conversation_id": conv.id,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_minutes": round(duration, 1),
                "message_count": len(conv.messages)
            })
    
    # Progress calculation breakdown
    completion_factors = {
        'conversations': min(total_conversations * 20, 30),
        'messages': min(total_messages * 2, 25),
        'memory': min(memory_count * 15, 30),
        'time': min(total_time / 2, 15)
    }
    
    total_completion = min(sum(completion_factors.values()), 100.0)
    
    return {
        "user_id": current_user.id,
        "module_id": module_id,
        "raw_data": {
            "conversations_count": total_conversations,
            "messages_count": total_messages,
            "memory_summaries_count": memory_count,
            "total_time_minutes": round(total_time, 1)
        },
        "time_breakdown": time_breakdown,
        "completion_calculation": {
            "factors": completion_factors,
            "total_percentage": round(total_completion, 1),
            "formula": "min(conversations*20, 30) + min(messages*2, 25) + min(memory*15, 30) + min(time/2, 15)"
        },
        "database_queries_used": [
            "SELECT * FROM conversations WHERE user_id = ? AND module_id = ?",
            "SELECT * FROM messages WHERE conversation_id IN (?)",
            "SELECT * FROM memory_summaries WHERE user_id = ? AND module_id = ?",
            "All calculations use real timestamp differences and actual data counts"
        ]
    }
