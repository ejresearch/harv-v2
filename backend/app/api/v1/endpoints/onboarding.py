# backend/app/api/v1/endpoints/onboarding.py
"""
Onboarding API - Memory System Integration
Captures learning preferences for enhanced memory system personalization
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User, OnboardingSurvey

router = APIRouter()

# =========================================================================
# PYDANTIC SCHEMAS
# =========================================================================

class LearningPreferences(BaseModel):
    learning_style: str  # "visual", "auditory", "kinesthetic", "reading_writing", "mixed"
    pace_preference: str  # "slow", "moderate", "fast", "adaptive"
    interaction_style: str  # "questioning", "examples", "practice", "discussion"
    feedback_preference: str  # "immediate", "summary", "minimal", "detailed"

class CommunicationBackground(BaseModel):
    prior_experience: str  # "none", "basic", "some", "extensive"
    professional_context: str  # "academic", "business", "personal", "mixed"
    specific_interests: List[str]
    learning_goals: str

class PersonalityProfile(BaseModel):
    confidence_level: str  # "low", "moderate", "high"
    curiosity_style: str  # "deep_dive", "broad_exploration", "practical_focus"
    challenge_preference: str  # "gradual", "moderate", "challenging"
    social_learning: bool

class TechnicalPreferences(BaseModel):
    session_duration_preference: int  # minutes
    time_of_day_preference: str  # "morning", "afternoon", "evening", "flexible"
    reminder_frequency: str  # "daily", "weekly", "as_needed", "none"
    progress_tracking: str  # "detailed", "summary", "minimal"

class OnboardingSurveyRequest(BaseModel):
    # Core learning preferences
    learning_preferences: LearningPreferences
    communication_background: CommunicationBackground
    personality_profile: PersonalityProfile
    technical_preferences: TechnicalPreferences
    
    # Additional context
    motivation_reason: str
    success_definition: str
    potential_challenges: List[str]
    additional_notes: Optional[str] = None

    @validator('learning_preferences')
    def validate_learning_style(cls, v):
        valid_styles = ["visual", "auditory", "kinesthetic", "reading_writing", "mixed"]
        if v.learning_style not in valid_styles:
            raise ValueError(f"Learning style must be one of: {valid_styles}")
        return v

class OnboardingStatusResponse(BaseModel):
    completed: bool
    user_id: int
    completion_date: Optional[str] = None
    learning_profile_summary: Optional[Dict[str, Any]] = None
    memory_system_config: Optional[Dict[str, Any]] = None
    recommended_starting_module: Optional[int] = None
    personalization_ready: bool

class PersonalizedRecommendation(BaseModel):
    module_id: int
    module_title: str
    recommendation_reason: str
    difficulty_adjustment: str
    estimated_duration: int
    teaching_approach: str

# =========================================================================
# HELPER FUNCTIONS
# =========================================================================

def generate_memory_system_config(survey_data: OnboardingSurveyRequest) -> Dict[str, Any]:
    """Generate memory system configuration based on user preferences"""
    
    config = {
        "personalization_level": "high",
        "context_adaptation": True,
        "learning_style_weights": {},
        "teaching_parameters": {},
        "engagement_settings": {}
    }
    
    # Learning style configuration
    style = survey_data.learning_preferences.learning_style
    if style == "visual":
        config["learning_style_weights"] = {
            "visual_examples": 0.8,
            "diagrams_references": 0.7,
            "spatial_metaphors": 0.6,
            "text_based": 0.3
        }
    elif style == "auditory":
        config["learning_style_weights"] = {
            "verbal_explanations": 0.8,
            "discussion_prompts": 0.7,
            "rhythm_patterns": 0.5,
            "sound_analogies": 0.6
        }
    elif style == "kinesthetic":
        config["learning_style_weights"] = {
            "hands_on_examples": 0.8,
            "movement_metaphors": 0.6,
            "practical_applications": 0.9,
            "abstract_theory": 0.2
        }
    elif style == "reading_writing":
        config["learning_style_weights"] = {
            "text_analysis": 0.8,
            "written_exercises": 0.7,
            "note_taking_prompts": 0.6,
            "reading_suggestions": 0.8
        }
    else:  # mixed
        config["learning_style_weights"] = {
            "multimodal_approach": 0.9,
            "varied_examples": 0.8,
            "flexible_format": 0.7
        }
    
    # Pace configuration
    pace = survey_data.learning_preferences.pace_preference
    config["teaching_parameters"]["pacing"] = {
        "question_frequency": "high" if pace == "fast" else "moderate" if pace == "moderate" else "low",
        "concept_introduction_rate": pace,
        "review_frequency": "high" if pace == "slow" else "moderate",
        "skip_redundancy": pace == "fast"
    }
    
    # Interaction style
    interaction = survey_data.learning_preferences.interaction_style
    config["teaching_parameters"]["socratic_style"] = {
        "question_type": "probing" if interaction == "questioning" else "practical",
        "example_density": "high" if interaction == "examples" else "moderate",
        "practice_integration": interaction == "practice",
        "discussion_orientation": interaction == "discussion"
    }
    
    # Confidence-based adjustments
    confidence = survey_data.personality_profile.confidence_level
    config["engagement_settings"]["confidence_building"] = {
        "encouragement_frequency": "high" if confidence == "low" else "moderate",
        "challenge_level": "gradual" if confidence == "low" else "moderate" if confidence == "moderate" else "challenging",
        "mistake_handling": "supportive" if confidence == "low" else "corrective",
        "success_celebration": confidence == "low"
    }
    
    # Session preferences
    session_duration = survey_data.technical_preferences.session_duration_preference
    config["engagement_settings"]["session_management"] = {
        "target_duration": session_duration,
        "break_suggestions": session_duration > 45,
        "progress_checkpoints": max(1, session_duration // 15),
        "wrap_up_reminders": True
    }
    
    return config

def recommend_starting_module(survey_data: OnboardingSurveyRequest, db: Session) -> PersonalizedRecommendation:
    """Recommend the best starting module based on user profile"""
    
    from app.models.course import Module
    
    # Get available modules
    modules = db.query(Module).filter(Module.is_active == True).order_by(Module.id).all()
    
    if not modules:
        return None
    
    experience = survey_data.communication_background.prior_experience
    confidence = survey_data.personality_profile.confidence_level
    
    # Default to Module 1 but with personalized approach
    recommended_module = modules[0]
    
    # Adjust recommendation based on experience
    if experience == "extensive" and confidence == "high":
        # Look for intermediate modules
        intermediate_modules = [m for m in modules if m.difficulty_level == "intermediate"]
        if intermediate_modules:
            recommended_module = intermediate_modules[0]
    
    # Determine teaching approach
    interaction_style = survey_data.learning_preferences.interaction_style
    
    if interaction_style == "questioning":
        approach = "Heavy Socratic questioning with deep exploration"
    elif interaction_style == "examples":
        approach = "Rich examples with guided discovery"
    elif interaction_style == "practice":
        approach = "Practical applications with hands-on learning"
    else:
        approach = "Interactive discussion with collaborative learning"
    
    # Adjust difficulty
    if confidence == "low":
        difficulty_adjustment = "Gentler introduction with more support"
    elif confidence == "high":
        difficulty_adjustment = "Standard pace with challenging questions"
    else:
        difficulty_adjustment = "Balanced approach with encouragement"
    
    # Estimate duration based on preferences
    base_duration = recommended_module.estimated_duration or 45
    pace = survey_data.learning_preferences.pace_preference
    
    if pace == "slow":
        estimated_duration = int(base_duration * 1.3)
    elif pace == "fast":
        estimated_duration = int(base_duration * 0.8)
    else:
        estimated_duration = base_duration
    
    reason_factors = []
    
    if experience == "none":
        reason_factors.append("perfect for beginners")
    if confidence == "low":
        reason_factors.append("supportive learning environment")
    if interaction_style == "questioning":
        reason_factors.append("matches your curiosity-driven style")
    
    reason = f"This module is {', '.join(reason_factors) if reason_factors else 'well-suited for your profile'}"
    
    return PersonalizedRecommendation(
        module_id=recommended_module.id,
        module_title=recommended_module.title,
        recommendation_reason=reason,
        difficulty_adjustment=difficulty_adjustment,
        estimated_duration=estimated_duration,
        teaching_approach=approach
    )

# =========================================================================
# API ENDPOINTS
# =========================================================================

@router.post("/survey")
async def submit_onboarding_survey(
    survey_data: OnboardingSurveyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit onboarding survey and configure personalized learning
    Creates user profile for enhanced memory system integration
    """
    
    # Check if user already has completed onboarding
    existing_survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    # Serialize survey data
    preferences_json = survey_data.learning_preferences.dict()
    background_json = survey_data.communication_background.dict()
    personality_json = survey_data.personality_profile.dict()
    technical_json = survey_data.technical_preferences.dict()
    
    if existing_survey:
        # Update existing survey
        existing_survey.learning_style = survey_data.learning_preferences.learning_style
        existing_survey.pace_preference = survey_data.learning_preferences.pace_preference
        existing_survey.interaction_style = survey_data.learning_preferences.interaction_style
        existing_survey.prior_experience = survey_data.communication_background.prior_experience
        existing_survey.goals = survey_data.communication_background.learning_goals
        existing_survey.confidence_level = survey_data.personality_profile.confidence_level
        existing_survey.session_duration_preference = survey_data.technical_preferences.session_duration_preference
        existing_survey.updated_at = datetime.utcnow()
        
        survey = existing_survey
    else:
        # Create new survey
        survey = OnboardingSurvey(
            user_id=current_user.id,
            learning_style=survey_data.learning_preferences.learning_style,
            pace_preference=survey_data.learning_preferences.pace_preference,
            interaction_style=survey_data.learning_preferences.interaction_style,
            prior_experience=survey_data.communication_background.prior_experience,
            goals=survey_data.communication_background.learning_goals,
            confidence_level=survey_data.personality_profile.confidence_level,
            session_duration_preference=survey_data.technical_preferences.session_duration_preference,
            created_at=datetime.utcnow()
        )
        db.add(survey)
    
    # Generate memory system configuration
    memory_config = generate_memory_system_config(survey_data)
    
    # Update user profile with comprehensive onboarding data
    onboarding_profile = {
        "learning_preferences": preferences_json,
        "communication_background": background_json,
        "personality_profile": personality_json,
        "technical_preferences": technical_json,
        "motivation_reason": survey_data.motivation_reason,
        "success_definition": survey_data.success_definition,
        "potential_challenges": survey_data.potential_challenges,
        "memory_system_config": memory_config,
        "onboarding_completed": True,
        "completion_date": datetime.utcnow().isoformat()
    }
    
    current_user.onboarding_data = json.dumps(onboarding_profile)
    current_user.updated_at = datetime.utcnow()
    
    # Get personalized module recommendation
    recommendation = recommend_starting_module(survey_data, db)
    
    db.commit()
    db.refresh(survey)
    db.refresh(current_user)
    
    return {
        "status": "completed",
        "user_id": current_user.id,
        "completion_date": survey.created_at.isoformat(),
        "learning_profile_summary": {
            "learning_style": survey.learning_style,
            "pace": survey.pace_preference,
            "experience_level": survey.prior_experience,
            "confidence": survey.confidence_level,
            "preferred_session_duration": survey.session_duration_preference
        },
        "memory_system_configured": True,
        "personalization_enabled": True,
        "recommended_starting_module": recommendation.dict() if recommendation else None,
        "next_steps": [
            "Start with your recommended module",
            "Engage in Socratic dialogue",
            "Reflect on your learning insights",
            "Build cross-concept connections"
        ]
    }

@router.get("/status", response_model=OnboardingStatusResponse)
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current onboarding status and personalization configuration
    Shows if memory system is ready for enhanced experience
    """
    
    survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    completed = survey is not None
    
    # Parse onboarding data if available
    onboarding_data = None
    memory_config = None
    
    if current_user.onboarding_data:
        try:
            onboarding_data = json.loads(current_user.onboarding_data)
            memory_config = onboarding_data.get("memory_system_config")
        except (json.JSONDecodeError, TypeError):
            pass
    
    # Learning profile summary
    profile_summary = None
    if survey:
        profile_summary = {
            "learning_style": survey.learning_style,
            "pace_preference": survey.pace_preference,
            "interaction_style": survey.interaction_style,
            "prior_experience": survey.prior_experience,
            "confidence_level": survey.confidence_level,
            "session_duration": survey.session_duration_preference,
            "goals": survey.goals
        }
    
    # Determine recommended starting module
    recommended_module_id = None
    if completed and onboarding_data:
        # Could store recommendation in onboarding data or calculate dynamically
        from app.models.course import Module
        modules = db.query(Module).filter(Module.is_active == True).order_by(Module.id).limit(1).all()
        if modules:
            recommended_module_id = modules[0].id
    
    return OnboardingStatusResponse(
        completed=completed,
        user_id=current_user.id,
        completion_date=survey.created_at.isoformat() if survey else None,
        learning_profile_summary=profile_summary,
        memory_system_config=memory_config,
        recommended_starting_module=recommended_module_id,
        personalization_ready=completed and memory_config is not None
    )

@router.get("/profile/detailed")
async def get_detailed_learning_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed learning profile for memory system configuration
    Used by enhanced memory system to personalize teaching approach
    """
    
    survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Onboarding not completed")
    
    # Get full onboarding data
    onboarding_data = {}
    if current_user.onboarding_data:
        try:
            onboarding_data = json.loads(current_user.onboarding_data)
        except (json.JSONDecodeError, TypeError):
            pass
    
    return {
        "user_id": current_user.id,
        "basic_profile": {
            "learning_style": survey.learning_style,
            "pace_preference": survey.pace_preference,
            "interaction_style": survey.interaction_style,
            "prior_experience": survey.prior_experience,
            "confidence_level": survey.confidence_level,
            "goals": survey.goals
        },
        "memory_system_config": onboarding_data.get("memory_system_config", {}),
        "teaching_preferences": {
            "session_duration": survey.session_duration_preference,
            "feedback_style": onboarding_data.get("learning_preferences", {}).get("feedback_preference", "detailed"),
            "challenge_level": onboarding_data.get("personality_profile", {}).get("challenge_preference", "moderate"),
            "social_learning": onboarding_data.get("personality_profile", {}).get("social_learning", False)
        },
        "motivation_context": {
            "reason": onboarding_data.get("motivation_reason", ""),
            "success_definition": onboarding_data.get("success_definition", ""),
            "potential_challenges": onboarding_data.get("potential_challenges", [])
        },
        "personalization_ready": True,
        "last_updated": survey.updated_at.isoformat() if survey.updated_at else survey.created_at.isoformat()
    }

@router.put("/preferences/update")
async def update_learning_preferences(
    preferences_update: LearningPreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update specific learning preferences
    Allows users to refine their profile as they learn more about their preferences
    """
    
    survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Complete onboarding survey first")
    
    # Update survey record
    survey.learning_style = preferences_update.learning_style
    survey.pace_preference = preferences_update.pace_preference  
    survey.interaction_style = preferences_update.interaction_style
    survey.updated_at = datetime.utcnow()
    
    # Update onboarding data
    if current_user.onboarding_data:
        try:
            onboarding_data = json.loads(current_user.onboarding_data)
            onboarding_data["learning_preferences"].update(preferences_update.dict())
            
            # Regenerate memory system config with new preferences
            survey_data = OnboardingSurveyRequest(
                learning_preferences=preferences_update,
                communication_background=CommunicationBackground(**onboarding_data["communication_background"]),
                personality_profile=PersonalityProfile(**onboarding_data["personality_profile"]),
                technical_preferences=TechnicalPreferences(**onboarding_data["technical_preferences"]),
                motivation_reason=onboarding_data["motivation_reason"],
                success_definition=onboarding_data["success_definition"],
                potential_challenges=onboarding_data["potential_challenges"]
            )
            
            new_memory_config = generate_memory_system_config(survey_data)
            onboarding_data["memory_system_config"] = new_memory_config
            onboarding_data["last_preferences_update"] = datetime.utcnow().isoformat()
            
            current_user.onboarding_data = json.dumps(onboarding_data)
            current_user.updated_at = datetime.utcnow()
            
        except (json.JSONDecodeError, TypeError, KeyError) as e:
            raise HTTPException(status_code=400, detail=f"Error updating preferences: {str(e)}")
    
    db.commit()
    db.refresh(survey)
    db.refresh(current_user)
    
    return {
        "status": "preferences_updated",
        "updated_preferences": preferences_update.dict(),
        "memory_system_reconfigured": True,
        "updated_at": survey.updated_at.isoformat(),
        "message": "Your learning preferences have been updated. The memory system will now personalize your experience accordingly."
    }

@router.get("/recommendations/modules")
async def get_module_recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized module recommendations based on learning profile
    Considers user progress, preferences, and learning patterns
    """
    
    survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    if not survey:
        return {
            "recommendations": [],
            "message": "Complete onboarding survey for personalized recommendations"
        }
    
    from app.models.course import Module
    from app.models.conversation import Conversation, UserProgress
    
    # Get all modules and user progress
    all_modules = db.query(Module).filter(Module.is_active == True).all()
    user_progress = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
    user_conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    
    # Create progress lookup
    progress_lookup = {p.module_id: p for p in user_progress}
    modules_with_conversations = set(conv.module_id for conv in user_conversations)
    
    recommendations = []
    
    for module in all_modules:
        progress = progress_lookup.get(module.id)
        has_conversations = module.id in modules_with_conversations
        
        # Determine recommendation type
        if not has_conversations:
            rec_type = "not_started"
            priority = "high" if module.id == 1 else "medium"  # First module gets high priority
        elif progress and progress.completion_percentage >= 80:
            rec_type = "completed"
            priority = "low"
        elif progress and progress.completion_percentage >= 20:
            rec_type = "in_progress"
            priority = "high"
        else:
            rec_type = "started"
            priority = "medium"
        
        # Skip completed modules for recommendations
        if rec_type == "completed":
            continue
        
        # Generate personalized reason
        reason_parts = []
        
        if rec_type == "not_started":
            if module.id == 1:
                reason_parts.append("Perfect starting point for your learning journey")
            else:
                reason_parts.append("Next logical step in your communication learning path")
        elif rec_type == "in_progress":
            reason_parts.append("Continue your active learning progress")
        else:
            reason_parts.append("Build on your initial exploration")
        
        # Add learning style specific reasons
        if survey.learning_style == "visual" and "models" in module.title.lower():
            reason_parts.append("includes visual communication models you'll enjoy")
        elif survey.learning_style == "kinesthetic" and "practice" in module.description.lower():
            reason_parts.append("offers hands-on learning experiences")
        
        # Add experience-based reasons
        if survey.prior_experience == "none" and module.difficulty_level == "beginner":
            reason_parts.append("designed for beginners like you")
        elif survey.prior_experience == "extensive" and module.difficulty_level == "advanced":
            reason_parts.append("matches your advanced experience level")
        
        reason = "; ".join(reason_parts)
        
        # Adjust teaching approach
        if survey.confidence_level == "low":
            approach = "Gentle introduction with plenty of support and encouragement"
        elif survey.confidence_level == "high":
            approach = "Challenging exploration with advanced questioning"
        else:
            approach = "Balanced approach with guided discovery"
        
        # Estimate duration based on pace preference
        base_duration = module.estimated_duration or 45
        if survey.pace_preference == "slow":
            estimated_duration = int(base_duration * 1.4)
        elif survey.pace_preference == "fast":
            estimated_duration = int(base_duration * 0.7)
        else:
            estimated_duration = base_duration
        
        recommendation = PersonalizedRecommendation(
            module_id=module.id,
            module_title=module.title,
            recommendation_reason=reason,
            difficulty_adjustment=approach,
            estimated_duration=estimated_duration,
            teaching_approach=f"{survey.interaction_style.title()}-focused learning"
        )
        
        recommendations.append({
            **recommendation.dict(),
            "priority": priority,
            "status": rec_type,
            "completion_percentage": progress.completion_percentage if progress else 0.0
        })
    
    # Sort by priority (high -> medium -> low) and then by module order
    priority_order = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda x: (priority_order[x["priority"]], x["module_id"]))
    
    return {
        "user_id": current_user.id,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations,
        "personalization_factors": {
            "learning_style": survey.learning_style,
            "pace_preference": survey.pace_preference,
            "interaction_style": survey.interaction_style,
            "confidence_level": survey.confidence_level,
            "prior_experience": survey.prior_experience
        },
        "generated_at": datetime.utcnow().isoformat()
    }
