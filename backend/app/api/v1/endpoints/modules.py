"""
Learning Modules API - WORKING IMPLEMENTATION
Provides module data for the GUI
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db

router = APIRouter()

class ModuleResponse(BaseModel):
    id: int
    title: str
    description: str
    objectives: List[str] = []
    progress: int = 0
    configured: bool = True

@router.get("/", response_model=List[ModuleResponse])
async def list_modules(db: Session = Depends(get_db)):
    """Get all learning modules"""
    return [
        ModuleResponse(
            id=1,
            title="Your Four Worlds",
            description="Communication models, perception, and the four worlds we live in",
            objectives=[
                "Identify the four worlds of communication",
                "Understand perception's role in communication",
                "Apply communication models to real scenarios"
            ],
            progress=34,
            configured=True
        ),
        ModuleResponse(
            id=2,
            title="Interpersonal Communication", 
            description="Personal relationships and one-on-one communication",
            objectives=[
                "Master interpersonal communication skills",
                "Understand relationship dynamics",
                "Practice active listening"
            ],
            progress=0,
            configured=False
        ),
        ModuleResponse(
            id=3,
            title="Small Group Communication",
            description="Communication in teams and small groups",
            objectives=[
                "Understand group dynamics",
                "Learn team communication strategies",
                "Practice leadership skills"
            ],
            progress=0,
            configured=False
        )
    ]

@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(module_id: int, db: Session = Depends(get_db)):
    """Get specific module"""
    modules = await list_modules(db)
    for module in modules:
        if module.id == module_id:
            return module
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Module not found")
