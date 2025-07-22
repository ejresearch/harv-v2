# backend/app/api/v1/endpoints/modules.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User
from ....models.course import Module
from ....models.conversation import Conversation, Message
from ....models.memory import UserProgress, MemorySummary

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
    system_prompt: Optional[str] = None
    module_prompt: Optional[str] = None

    class Config:
        from_attributes = True

@router.get("/", response_model=List[ModuleResponse])
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all modules with REAL user progress from database"""
    try:
        # Get all active modules
        modules = db.query(Module).filter(Module.is_active == True).all()
        
        result = []
        for module in modules:
            # Get REAL progress from UserProgress table
            progress = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.module_id == module.id
            ).first()
            
            # Count REAL conversations for this module
            conversations_count = db.query(Conversation).filter(
                Conversation.user_id == current_user.id,
                Conversation.module_id == module.id
            ).count()
            
            # Count REAL messages
            messages_count = db.query(Message).join(Conversation).filter(
                Conversation.user_id == current_user.id,
                Conversation.module_id == module.id
            ).count()
            
            # Get REAL memory summaries for objective completion
            memory_summaries = db.query(MemorySummary).filter(
                MemorySummary.user_id == current_user.id,
                MemorySummary.module_id == module.id
            ).count()
            
            # Calculate REAL completion percentage from actual data
            objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
            objectives_completed = min(memory_summaries, len(objectives))
            completion_percentage = (objectives_completed / max(len(objectives), 1)) * 100 if objectives else 0
            
            # Update or create progress record with real data
            if progress:
                progress.completion_percentage = completion_percentage
                progress.total_conversations = conversations_count
                progress.total_messages = messages_count
            else:
                progress = UserProgress(
                    user_id=current_user.id,
                    module_id=module.id,
                    completion_percentage=completion_percentage,
                    total_conversations=conversations_count,
                    total_messages=messages_count,
                    mastery_level="beginner"
                )
                db.add(progress)
            
            db.commit()
            
            # Build response with REAL user progress data
            result.append(ModuleResponse(
                id=module.id,
                title=module.title,
                description=module.description,
                learning_objectives=objectives,
                difficulty_level=module.difficulty_level,
                estimated_duration=module.estimated_duration,
                resources=module.resources,
                system_prompt=module.system_prompt,
                module_prompt=module.module_prompt,
                user_progress={
                    "completion_percentage": completion_percentage,
                    "conversations_count": conversations_count,
                    "messages_count": messages_count,
                    "objectives_completed": objectives_completed,
                    "total_objectives": len(objectives),
                    "mastery_level": progress.mastery_level,
                    "last_accessed": progress.updated_at.isoformat() if progress.updated_at else None,
                    "time_spent_minutes": progress.time_spent if progress and progress.time_spent else 0
                }
            ))
        
        return result
    
    except Exception as e:
        # Fallback to basic module info if there are any issues
        modules = db.query(Module).filter(Module.is_active == True).all()
        fallback_result = []
        
        for module in modules:
            objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
            fallback_result.append(ModuleResponse(
                id=module.id,
                title=module.title,
                description=module.description,
                learning_objectives=objectives,
                difficulty_level=module.difficulty_level,
                estimated_duration=module.estimated_duration,
                resources=module.resources,
                user_progress={
                    "completion_percentage": 0.0,
                    "conversations_count": 0,
                    "messages_count": 0,
                    "objectives_completed": 0,
                    "total_objectives": len(objectives),
                    "mastery_level": "beginner",
                    "time_spent_minutes": 0
                }
            ))
        
        return fallback_result

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module_details(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed module info with REAL progress data"""
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    try:
        # Real progress calculation from actual database data
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.module_id == module_id
        ).first()
        
        # Real conversation count
        total_conversations = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.module_id == module_id
        ).count()
        
        # Real message count from actual conversations
        total_messages = 0
        conversations = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.module_id == module_id
        ).all()
        
        total_time_spent = 0
        for conv in conversations:
            messages_in_conv = db.query(Message).filter(Message.conversation_id == conv.id).count()
            total_messages += messages_in_conv
            
            # Calculate time from conversation timestamps
            if conv.messages:
                start_time = conv.created_at
                end_time = conv.updated_at or conv.created_at
                duration_minutes = (end_time - start_time).total_seconds() / 60
                total_time_spent += max(duration_minutes, 5)  # Minimum 5 minutes
        
        # Real memory summaries (objectives completed)
        memory_summaries_count = db.query(MemorySummary).filter(
            MemorySummary.user_id == current_user.id,
            MemorySummary.module_id == module_id
        ).count()
        
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        completion_percentage = (memory_summaries_count / max(len(objectives), 1)) * 100
        
        # Update progress with real data
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                module_id=module_id,
                completion_percentage=completion_percentage,
                total_conversations=total_conversations,
                total_messages=total_messages,
                time_spent=int(total_time_spent),
                mastery_level="beginner"
            )
            db.add(progress)
            db.commit()
        else:
            progress.completion_percentage = completion_percentage
            progress.total_conversations = total_conversations
            progress.total_messages = total_messages
            progress.time_spent = int(total_time_spent)
            db.commit()
        
        return ModuleResponse(
            id=module.id,
            title=module.title,
            description=module.description,
            learning_objectives=objectives,
            difficulty_level=module.difficulty_level,
            estimated_duration=module.estimated_duration,
            resources=module.resources,
            system_prompt=module.system_prompt,
            module_prompt=module.module_prompt,
            user_progress={
                "completion_percentage": completion_percentage,
                "conversations_count": total_conversations,
                "messages_count": total_messages,
                "objectives_completed": memory_summaries_count,
                "total_objectives": len(objectives),
                "mastery_level": progress.mastery_level,
                "time_spent_minutes": int(total_time_spent),
                "last_accessed": progress.updated_at.isoformat() if progress.updated_at else None
            }
        )
        
    except Exception as e:
        # Fallback with basic module info
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        return ModuleResponse(
            id=module.id,
            title=module.title,
            description=module.description,
            learning_objectives=objectives,
            difficulty_level=module.difficulty_level,
            estimated_duration=module.estimated_duration,
            resources=module.resources,
            user_progress={
                "completion_percentage": 0.0,
                "conversations_count": 0,
                "messages_count": 0,
                "objectives_completed": 0,
                "total_objectives": len(objectives),
                "mastery_level": "beginner",
                "time_spent_minutes": 0
            }
        )


# backend/app/api/v1/endpoints/progress.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Dict, Any
import json

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User
from ....models.course import Module
from ....models.conversation import Conversation, Message
from ....models.memory import UserProgress, MemorySummary

router = APIRouter()

class ProgressResponse(BaseModel):
    module_id: int
    completion_percentage: float
    objectives_completed: List[str]
    objectives_in_progress: List[str]
    objectives_not_started: List[str]
    total_conversations: int
    total_messages: int
    time_spent_minutes: int
    memory_summaries_count: int
    mastery_level: str
    recent_activity: List[Dict[str, Any]]
    learning_insights: Dict[str, Any]

@router.get("/{module_id}", response_model=ProgressResponse)
async def get_module_progress(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get REAL progress calculated from actual database data"""
    
    # Get the module
    module = db.query(Module).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    try:
        # Get all REAL conversations for this user/module
        conversations = db.query(Conversation).filter(
            Conversation.user_id == current_user.id,
            Conversation.module_id == module_id
        ).order_by(Conversation.created_at.desc()).all()
        
        # Calculate REAL metrics from database
        total_messages = 0
        total_time_spent = 0
        recent_activity = []
        
        for conv in conversations:
            # Count messages in this conversation
            messages = db.query(Message).filter(Message.conversation_id == conv.id).all()
            messages_count = len(messages)
            total_messages += messages_count
            
            # Calculate time from first to last message
            if messages:
                start_time = messages[0].created_at
                end_time = messages[-1].created_at
                duration_minutes = max((end_time - start_time).total_seconds() / 60, 5)
                total_time_spent += duration_minutes
            else:
                duration_minutes = 5  # Minimum time for conversation
                total_time_spent += duration_minutes
            
            # Add to recent activity (limit to last 5 conversations)
            if len(recent_activity) < 5:
                recent_activity.append({
                    "conversation_id": conv.id,
                    "title": conv.title or f"Session {len(recent_activity) + 1}",
                    "message_count": messages_count,
                    "duration_minutes": int(duration_minutes),
                    "date": conv.created_at.strftime("%Y-%m-%d"),
                    "time": conv.created_at.strftime("%H:%M"),
                    "summary": conv.memory_summary[:100] + "..." if conv.memory_summary else "Learning session completed"
                })
        
        # Get REAL memory summaries (completed objectives)
        memory_summaries = db.query(MemorySummary).filter(
            MemorySummary.user_id == current_user.id,
            MemorySummary.module_id == module_id
        ).all()
        
        # Parse learning objectives
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        
        # Determine objective completion based on REAL data
        objectives_completed = []
        objectives_in_progress = []
        objectives_not_started = []
        
        # Simple completion logic based on memory summaries and message count
        completed_count = len(memory_summaries)
        
        for i, objective in enumerate(objectives):
            if i < completed_count:
                objectives_completed.append(objective)
            elif i == completed_count and total_messages >= (i + 1) * 5:  # In progress if enough messages
                objectives_in_progress.append(objective)
            else:
                objectives_not_started.append(objective)
        
        # Calculate completion percentage
        completion_percentage = (len(objectives_completed) / max(len(objectives), 1)) * 100
        
        # Determine mastery level based on completion and engagement
        if completion_percentage >= 90:
            mastery_level = "advanced"
        elif completion_percentage >= 60:
            mastery_level = "intermediate"
        else:
            mastery_level = "beginner"
        
        # Generate learning insights
        avg_messages_per_conversation = total_messages / max(len(conversations), 1)
        learning_insights = {
            "engagement_level": "high" if avg_messages_per_conversation >= 15 else "moderate" if avg_messages_per_conversation >= 8 else "low",
            "learning_pace": "fast" if completion_percentage >= 20 and len(conversations) <= 3 else "steady",
            "strength_areas": objectives_completed[:2] if objectives_completed else [],
            "focus_recommendations": objectives_in_progress[:1] + objectives_not_started[:1] if objectives_in_progress or objectives_not_started else [],
            "total_learning_time": int(total_time_spent),
            "average_session_length": int(total_time_spent / max(len(conversations), 1))
        }
        
        # Update or create progress record
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.module_id == module_id
        ).first()
        
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                module_id=module_id,
                completion_percentage=completion_percentage,
                total_conversations=len(conversations),
                total_messages=total_messages,
                time_spent=int(total_time_spent),
                mastery_level=mastery_level
            )
            db.add(progress)
        else:
            progress.completion_percentage = completion_percentage
            progress.total_conversations = len(conversations)
            progress.total_messages = total_messages
            progress.time_spent = int(total_time_spent)
            progress.mastery_level = mastery_level
        
        db.commit()
        
        return ProgressResponse(
            module_id=module_id,
            completion_percentage=completion_percentage,
            objectives_completed=objectives_completed,
            objectives_in_progress=objectives_in_progress,
            objectives_not_started=objectives_not_started,
            total_conversations=len(conversations),
            total_messages=total_messages,
            time_spent_minutes=int(total_time_spent),
            memory_summaries_count=len(memory_summaries),
            mastery_level=mastery_level,
            recent_activity=recent_activity,
            learning_insights=learning_insights
        )
        
    except Exception as e:
        # Fallback response with basic info
        objectives = json.loads(module.learning_objectives) if module.learning_objectives else []
        return ProgressResponse(
            module_id=module_id,
            completion_percentage=0.0,
            objectives_completed=[],
            objectives_in_progress=[],
            objectives_not_started=objectives,
            total_conversations=0,
            total_messages=0,
            time_spent_minutes=0,
            memory_summaries_count=0,
            mastery_level="beginner",
            recent_activity=[],
            learning_insights={
                "engagement_level": "not_started",
                "learning_pace": "not_started",
                "strength_areas": [],
                "focus_recommendations": objectives[:2],
                "total_learning_time": 0,
                "average_session_length": 0
            }
        )


# backend/app/api/v1/endpoints/onboarding.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import json

from ....core.database import get_db
from ....core.security import get_current_user
from ....models.user import User, OnboardingSurvey

router = APIRouter()

class OnboardingSurveyCreate(BaseModel):
    learning_style: str  # "visual", "auditory", "kinesthetic", "reading"
    goals: str
    preferred_pace: str  # "slow", "medium", "fast"
    interaction_preference: str  # "questions", "examples", "practice"
    background_info: str
    prior_experience: str
    communication_challenges: Optional[str] = None
    preferred_examples: Optional[str] = None  # "business", "academic", "personal", "technical"

class OnboardingResponse(BaseModel):
    completed: bool
    learning_profile: Optional[dict] = None
    memory_system_configured: bool
    ready_for_modules: bool

@router.post("/survey")
async def submit_onboarding_survey(
    survey_data: OnboardingSurveyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save onboarding survey for memory system personalization"""
    
    try:
        # Check if survey already exists
        existing_survey = db.query(OnboardingSurvey).filter(
            OnboardingSurvey.user_id == current_user.id
        ).first()
        
        if existing_survey:
            # Update existing survey
            for field, value in survey_data.dict().items():
                setattr(existing_survey, field, value)
            survey = existing_survey
        else:
            # Create new survey
            survey = OnboardingSurvey(
                user_id=current_user.id,
                **survey_data.dict()
            )
            db.add(survey)
        
        # Update user's onboarding data for memory system
        memory_config = {
            "learning_style": survey_data.learning_style,
            "preferred_pace": survey_data.preferred_pace,
            "interaction_preference": survey_data.interaction_preference,
            "goals": survey_data.goals,
            "background": survey_data.background_info,
            "challenges": survey_data.communication_challenges,
            "example_preference": survey_data.preferred_examples
        }
        
        current_user.onboarding_data = json.dumps(memory_config)
        
        db.commit()
        db.refresh(survey)
        
        return {
            "status": "completed",
            "message": "Onboarding survey saved successfully",
            "learning_profile": {
                "style": survey.learning_style,
                "pace": survey.preferred_pace,
                "goals": survey.goals,
                "interaction_preference": survey.interaction_preference
            },
            "memory_system_configured": True,
            "ready_for_modules": True,
            "personalization_active": True
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to save onboarding survey: {str(e)}",
            "memory_system_configured": False,
            "ready_for_modules": False
        }

@router.get("/status", response_model=OnboardingResponse)
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if user completed onboarding and get learning profile"""
    
    try:
        survey = db.query(OnboardingSurvey).filter(
            OnboardingSurvey.user_id == current_user.id
        ).first()
        
        if survey:
            learning_profile = {
                "learning_style": survey.learning_style,
                "preferred_pace": survey.preferred_pace,
                "goals": survey.goals,
                "interaction_preference": survey.interaction_preference,
                "background_info": survey.background_info,
                "prior_experience": survey.prior_experience,
                "communication_challenges": survey.communication_challenges,
                "preferred_examples": survey.preferred_examples
            }
            
            return OnboardingResponse(
                completed=True,
                learning_profile=learning_profile,
                memory_system_configured=True,
                ready_for_modules=True
            )
        else:
            return OnboardingResponse(
                completed=False,
                learning_profile=None,
                memory_system_configured=False,
                ready_for_modules=False
            )
            
    except Exception as e:
        return OnboardingResponse(
            completed=False,
            learning_profile=None,
            memory_system_configured=False,
            ready_for_modules=False
        )

@router.get("/memory-config")
async def get_memory_configuration(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's memory system configuration for 4-layer context assembly"""
    
    try:
        survey = db.query(OnboardingSurvey).filter(
            OnboardingSurvey.user_id == current_user.id
        ).first()
        
        if survey:
            # Memory system configuration for Layer 1 (User Profile)
            memory_config = {
                "user_profile": {
                    "name": current_user.name,
                    "learning_style": survey.learning_style,
                    "preferred_pace": survey.preferred_pace,
                    "interaction_preference": survey.interaction_preference,
                    "background": survey.background_info,
                    "goals": survey.goals,
                    "challenges": survey.communication_challenges,
                    "example_preference": survey.preferred_examples or "mixed"
                },
                "teaching_adaptations": {
                    "question_style": "discovery-based" if survey.interaction_preference == "questions" else "example-driven",
                    "pace_modifier": survey.preferred_pace,
                    "content_focus": survey.goals,
                    "challenge_areas": survey.communication_challenges
                },
                "socratic_parameters": {
                    "complexity_level": "high" if "advanced" in survey.prior_experience.lower() else "moderate",
                    "real_world_focus": survey.preferred_examples,
                    "personal_connection": survey.background_info
                }
            }
            
            return {
                "configured": True,
                "memory_config": memory_config,
                "last_updated": survey.updated_at.isoformat() if survey.updated_at else survey.created_at.isoformat()
            }
        else:
            # Default configuration for users without onboarding
            return {
                "configured": False,
                "memory_config": {
                    "user_profile": {
                        "name": current_user.name,
                        "learning_style": "mixed",
                        "preferred_pace": "medium",
                        "interaction_preference": "balanced",
                        "background": "general",
                        "goals": "improve communication skills"
                    },
                    "teaching_adaptations": {
                        "question_style": "balanced",
                        "pace_modifier": "medium",
                        "content_focus": "general communication improvement"
                    },
                    "socratic_parameters": {
                        "complexity_level": "moderate",
                        "real_world_focus": "mixed",
                        "personal_connection": "general"
                    }
                }
            }
            
    except Exception as e:
        return {
            "configured": False,
            "error": str(e),
            "memory_config": None
        }
