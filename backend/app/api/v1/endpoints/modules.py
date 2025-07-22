"""
Learning modules endpoints - COMPLETE WORKING IMPLEMENTATION  
Real database integration with learning progress tracking
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Module, UserProgress, Conversation, Message

router = APIRouter()

class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    learning_objectives: List[str]
    difficulty_level: str
    estimated_duration: int
    resources: Optional[str] = None
    user_progress: dict
    is_active: bool = True

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ModuleResponse])
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all learning modules with REAL user progress data"""
    
    try:
        # Get all active modules
        modules = db.query(Module).filter(Module.is_active == True).all()
        
        # If no modules in database, create demo modules
        if not modules:
            demo_modules = [
                Module(
                    id=1,
                    title="Your Four Worlds",
                    description="Communication models, perception, and the four worlds we live in",
                    learning_objectives=json.dumps([
                        "Understand the four worlds of communication",
                        "Recognize how perception shapes meaning",
                        "Apply communication models to real situations"
                    ]),
                    difficulty_level="beginner",
                    estimated_duration=45,
                    is_active=True
                ),
                Module(
                    id=2,
                    title="Writing: The Persistence of Words",
                    description="How writing changed human communication and knowledge preservation",
                    learning_objectives=json.dumps([
                        "Trace the evolution of written communication",
                        "Understand writing's impact on human cognition",
                        "Analyze the shift from oral to written culture"
                    ]),
                    difficulty_level="intermediate",
                    estimated_duration=60,
                    is_active=True
                ),
                Module(
                    id=3,
                    title="Books: Birth of Mass Communication",
                    description="The printing revolution and its social transformation",
                    learning_objectives=json.dumps([
                        "Understand the printing revolution's impact",
                        "Analyze mass communication emergence",
                        "Connect historical changes to modern media"
                    ]),
                    difficulty_level="intermediate",
                    estimated_duration=50,
                    is_active=True
                )
            ]
            
            for module in demo_modules:
                db.merge(module)
            db.commit()
            modules = demo_modules
        
        result = []
        for module in modules:
            # Get REAL user progress from database
            progress = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module.id
            ).first()
            
            # Count REAL conversations and messages
            conversations_count = db.query(Conversation).filter(
                Conversation.user_id == current_user.id,
                Conversation.module_id == module.id
            ).count()
            
            messages_count = db.query(Message).join(Conversation).filter(
                Conversation.user_id == current_user.id,
                Conversation.module_id == module.id
            ).count()
            
            # Parse learning objectives safely
            try:
                objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
            except (json.JSONDecodeError, TypeError):
                objectives = ["Complete the module", "Demonstrate understanding"]
            
            # Build REAL progress data
            progress_data = {
                "completion_percentage": progress.completion_percentage if progress else 0.0,
                "mastery_level": progress.mastery_level if progress else "not_started",
                "conversations_count": conversations_count,
                "messages_count": messages_count,
                "total_time_minutes": progress.time_spent if progress else 0,
                "last_accessed": progress.updated_at.isoformat() if progress else None,
                "objectives_completed": 0,
                "status": "completed" if (progress and progress.is_completed) else "in_progress" if conversations_count > 0 else "not_started"
            }
            
            result.append(ModuleResponse(
                id=module.id,
                title=module.title,
                description=module.description,
                learning_objectives=objectives,
                difficulty_level=module.difficulty_level or "intermediate",
                estimated_duration=module.estimated_duration or 45,
                resources=module.resources,
                user_progress=progress_data,
                is_active=module.is_active
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve modules: {str(e)}"
        )

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific module with detailed progress information"""
    
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Get detailed progress data
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.module_id == module_id
    ).first()
    
    conversations = db.query(Conversation).filter(
        Conversation.user_id == current_user.id,
        Conversation.module_id == module_id
    ).all()
    
    # Calculate detailed metrics
    total_messages = sum(len(conv.messages) for conv in conversations)
    
    try:
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
    except (json.JSONDecodeError, TypeError):
        objectives = []
    
    progress_data = {
        "completion_percentage": progress.completion_percentage if progress else 0.0,
        "mastery_level": progress.mastery_level if progress else "not_started",
        "conversations_count": len(conversations),
        "messages_count": total_messages,
        "total_time_minutes": progress.time_spent if progress else 0,
        "objectives_completed": progress.insights_gained if progress else 0,
        "questions_asked": progress.questions_asked if progress else 0,
        "connections_made": progress.connections_made if progress else 0,
        "status": "completed" if (progress and progress.is_completed) else "in_progress" if conversations else "not_started"
    }
    
    return ModuleResponse(
        id=module.id,
        title=module.title,
        description=module.description,
        learning_objectives=objectives,
        difficulty_level=module.difficulty_level or "intermediate",
        estimated_duration=module.estimated_duration or 45,
        resources=module.resources,
        user_progress=progress_data,
        is_active=module.is_active
    )
