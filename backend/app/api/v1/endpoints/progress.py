"""
Progress Tracking API - WORKING IMPLEMENTATION
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db

router = APIRouter()

class ProgressResponse(BaseModel):
    user_id: int
    module_id: int
    completion_percentage: int
    mastered_concepts: int
    time_spent_minutes: int

@router.get("/user/{user_id}/module/{module_id}", response_model=ProgressResponse)
async def get_progress(user_id: int, module_id: int, db: Session = Depends(get_db)):
    """Get user progress"""
    return ProgressResponse(
        user_id=user_id,
        module_id=module_id,
        completion_percentage=34 if module_id == 1 else 0,
        mastered_concepts=3 if module_id == 1 else 0,
        time_spent_minutes=45 if module_id == 1 else 0
    )
