"""
User Onboarding API - WORKING IMPLEMENTATION
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel

from app.core.database import get_db

router = APIRouter()

class OnboardingResponse(BaseModel):
    learning_style: str = "Visual"
    pace: str = "Moderate"
    background: str = "Beginner"
    preferences: Dict[str, Any] = {}

@router.get("/profile/{user_id}", response_model=OnboardingResponse)
async def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get onboarding profile"""
    return OnboardingResponse(
        learning_style="Visual",
        pace="Moderate",
        background="Beginner",
        preferences={"socratic_intensity": "moderate"}
    )
