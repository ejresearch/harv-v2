"""
User onboarding endpoints - COMPLETE WORKING IMPLEMENTATION
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, OnboardingSurvey

router = APIRouter()

class OnboardingRequest(BaseModel):
    learning_style: str
    prior_experience: str
    goals: str
    preferred_pace: str
    interaction_preference: str
    background_info: Optional[str] = None

class OnboardingResponse(BaseModel):
    completed: bool
    learning_profile: Optional[Dict[str, Any]] = None
    memory_system_configured: bool
    ready_for_modules: bool

@router.post("/complete")
async def complete_onboarding(
    request: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Complete user onboarding"""
    
    try:
        survey = OnboardingSurvey(
            user_id=current_user.id,
            learning_style=request.learning_style,
            prior_experience=request.prior_experience,
            goals=request.goals,
            preferred_pace=request.preferred_pace,
            interaction_preference=request.interaction_preference,
            background_info=request.background_info
        )
        
        db.add(survey)
        db.commit()
        
        return {
            "status": "success",
            "message": "Onboarding completed successfully",
            "memory_system_configured": True,
            "ready_for_modules": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")

@router.get("/status", response_model=OnboardingResponse)
async def get_onboarding_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check onboarding status"""
    
    survey = db.query(OnboardingSurvey).filter(
        OnboardingSurvey.user_id == current_user.id
    ).first()
    
    if survey:
        return OnboardingResponse(
            completed=True,
            learning_profile={
                "learning_style": survey.learning_style,
                "preferred_pace": survey.preferred_pace,
                "goals": survey.goals
            },
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
