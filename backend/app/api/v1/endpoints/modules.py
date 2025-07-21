"""
Modules API Endpoints
File: backend/app/api/v1/endpoints/modules.py
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User, Module

router = APIRouter()

class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    progress: float = 0.0
    is_active: bool = True

@router.get("/", response_model=List[ModuleResponse])
async def get_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all available learning modules"""
    try:
        modules = db.query(Module).filter(Module.is_active == True).all()
        
        if not modules:
            # Return demo modules if none in database
            return [
                ModuleResponse(
                    id=1,
                    title="Your Four Worlds",
                    description="Communication models, perception, and the four worlds we live in",
                    progress=0.0
                ),
                ModuleResponse(
                    id=2,
                    title="Writing: The Persistence of Words", 
                    description="How writing changed human communication and knowledge preservation",
                    progress=0.0
                ),
                ModuleResponse(
                    id=3,
                    title="Mass Communication",
                    description="Understanding mass media and its impact on society",
                    progress=0.0
                )
            ]
        
        return [
            ModuleResponse(
                id=module.id,
                title=module.title,
                description=module.description or f"Learning module: {module.title}",
                progress=0.0,
                is_active=module.is_active
            )
            for module in modules
        ]
        
    except Exception as e:
        # Fallback to demo data
        return [
            ModuleResponse(
                id=1,
                title="Communication Basics",
                description="Fundamental communication principles", 
                progress=0.0
            )
        ]

@router.get("/{module_id}")
async def get_module(
    module_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific module details"""
    try:
        module = db.query(Module).filter(Module.id == module_id).first()
        
        if not module:
            return {
                "id": module_id,
                "title": f"Module {module_id}",
                "description": "Demo learning module",
                "progress": 0.0
            }
        
        return {
            "id": module.id,
            "title": module.title,
            "description": module.description,
            "progress": 0.0,
            "learning_objectives": getattr(module, 'learning_objectives', 'Master key concepts'),
            "estimated_duration": getattr(module, 'estimated_duration', 45)
        }
        
    except Exception:
        return {
            "id": module_id,
            "title": f"Module {module_id}",
            "description": "Demo learning module",
            "progress": 0.0
        }
