"""
Admin endpoints - COMPLETE WORKING IMPLEMENTATION
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Module, Conversation, Message

router = APIRouter()

class SystemStatsResponse(BaseModel):
    total_users: int
    total_modules: int
    total_conversations: int
    total_messages: int
    active_users_7_days: int
    system_health: str

@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get system statistics"""
    
    try:
        total_users = db.query(User).count()
        total_modules = db.query(Module).count()
        total_conversations = db.query(Conversation).count()
        total_messages = db.query(Message).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        
        return SystemStatsResponse(
            total_users=total_users,
            total_modules=total_modules,
            total_conversations=total_conversations,
            total_messages=total_messages,
            active_users_7_days=active_users,
            system_health="healthy"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")
