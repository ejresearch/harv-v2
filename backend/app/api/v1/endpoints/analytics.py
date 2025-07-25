"""
Minimal Analytics Router - Phase 2.5
Prevents import errors while we build out the full analytics system
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def analytics_health():
    """Analytics system health check"""
    return {
        "status": "operational",
        "message": "Analytics system initialized",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "Learning progress tracking",
            "Socratic methodology analysis", 
            "Memory system performance",
            "Cross-module connections"
        ]
    }

@router.get("/overview")
async def get_analytics_overview(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get basic analytics overview"""
    return {
        "user_id": current_user.id,
        "message": "Analytics dashboard coming soon",
        "status": "development",
        "available_metrics": [
            "Total learning time",
            "Modules completed", 
            "Socratic compliance score",
            "Memory system effectiveness"
        ],
        "timestamp": datetime.now().isoformat()
    }
