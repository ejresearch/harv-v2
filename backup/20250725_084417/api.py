"""
Complete API Router - ALL ENDPOINTS INCLUDED
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    health,
    memory,
    chat,
    modules,
    progress,
    onboarding,
    admin
)

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(memory.router, prefix="/memory", tags=["enhanced-memory"])
api_router.include_router(chat.router, prefix="/chat", tags=["ai-chat"])
api_router.include_router(modules.router, prefix="/modules", tags=["learning-modules"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress-tracking"])
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["user-onboarding"])
api_router.include_router(admin.router, prefix="/admin", tags=["administration"])
