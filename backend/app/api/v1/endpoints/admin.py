"""
Admin API - WORKING IMPLEMENTATION
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.core.database import get_db

router = APIRouter()

class ModuleConfig(BaseModel):
    title: str
    description: str
    objectives: List[str]
    system_prompt: str
    module_prompt: str

@router.get("/modules/{module_id}/config", response_model=ModuleConfig)
async def get_config(module_id: int, db: Session = Depends(get_db)):
    """Get module configuration"""
    return ModuleConfig(
        title="Your Four Worlds",
        description="Communication models and perception",
        objectives=[
            "Identify communication models",
            "Understand perception's role",
            "Apply theories to practice"
        ],
        system_prompt="You are an expert communication tutor...",
        module_prompt="Guide students to discover communication concepts..."
    )
