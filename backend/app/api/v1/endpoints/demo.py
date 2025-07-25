"""
Demo Role Switching Endpoints
Allows seamless switching between student/teacher/admin perspectives
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User

router = APIRouter()

class RoleSwitchRequest(BaseModel):
    target_role: str  # 'student', 'educator', 'admin'
    maintain_session: bool = True

@router.post("/switch-role")
async def switch_demo_role(
    role_request: RoleSwitchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Switch between demo roles for comprehensive system exploration"""
    
    # Check if user has demo privileges
    if current_user.role != "universal" and current_user.email != "demo@harv.com":
        raise HTTPException(
            status_code=403,
            detail="Role switching only available for demo users"
        )
    
    valid_roles = ["student", "educator", "admin"]
    if role_request.target_role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    # Update user's current demo role
    current_user.demo_active_role = role_request.target_role
    db.commit()
    
    return {
        "success": True,
        "switched_to": role_request.target_role,
        "previous_role": getattr(current_user, 'previous_demo_role', 'student'),
        "message": f"Demo role switched to {role_request.target_role}. You now have access to {role_request.target_role} features."
    }

@router.get("/context/{role}")
async def get_role_demo_context(role: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get demo context and sample data for specific role"""
    
    contexts = {
        "student": {
            "dashboard_features": [
                "Learning progress tracking",
                "Socratic AI chat interface", 
                "Module completion status",
                "Memory system visualization",
                "Personal learning analytics"
            ],
            "sample_data": {
                "active_modules": 5,
                "completion_rate": "65%",
                "chat_sessions": 12,
                "learning_insights": 8
            }
        },
        "educator": {
            "dashboard_features": [
                "Student progress monitoring",
                "Module content management",
                "Socratic prompt configuration",
                "Learning analytics dashboard",
                "Content creation tools"
            ],
            "sample_data": {
                "total_students": 24,
                "active_modules": 15,
                "avg_engagement": "87%",
                "memory_insights": 156
            }
        },
        "admin": {
            "dashboard_features": [
                "System performance monitoring",
                "User management interface",
                "Database health tracking", 
                "Memory system analytics",
                "Configuration management"
            ],
            "sample_data": {
                "system_uptime": "99.9%",
                "total_users": 342,
                "api_response_time": "67ms",
                "memory_efficiency": "94%"
            }
        }
    }
    
    if role not in contexts:
        raise HTTPException(status_code=404, detail="Role context not found")
    
    return contexts[role]

@router.get("/available-features")
async def get_available_demo_features(current_user: User = Depends(get_current_user)):
    """Get all available features based on current demo role"""
    
    current_role = getattr(current_user, 'demo_active_role', current_user.role)
    
    feature_matrix = {
        "student": {
            "dashboard": "Student learning dashboard",
            "chat": "Socratic AI tutoring chat",
            "modules": "Learning module access",
            "progress": "Personal progress tracking",
            "memory": "Memory system visualization"
        },
        "educator": {
            "dashboard": "Educator analytics dashboard", 
            "students": "Student progress monitoring",
            "content": "Module content management",
            "analytics": "Learning effectiveness analytics",
            "prompts": "Socratic prompt configuration"
        },
        "admin": {
            "dashboard": "System administration dashboard",
            "users": "User account management", 
            "health": "System health monitoring",
            "database": "Database activity tracking",
            "config": "System configuration management"
        }
    }
    
    return {
        "current_role": current_role,
        "available_features": feature_matrix.get(current_role, {}),
        "can_switch_roles": current_user.role == "universal",
        "demo_mode": True
    }
