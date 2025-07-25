"""
API v1 Router - Phase 2.5 Fixed Version
Handles missing modules gracefully during development
"""

from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

# Import core modules that should already exist
from app.api.v1.endpoints import auth, users, health, memory

api_router = APIRouter()

# Core authentication and user management
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Phase 2: Enhanced Memory System
api_router.include_router(memory.router, prefix="/memory", tags=["enhanced-memory"])

# Phase 2.5: OpenAI Integration & Real-time Chat
try:
    from app.api.v1.endpoints import chat
    api_router.include_router(chat.router, prefix="/chat", tags=["ai-tutoring"])
    logger.info("✅ Chat endpoints loaded")
except (ImportError, AttributeError) as e:
    logger.warning(f"⚠️ Chat endpoints not available: {e}")

# Phase 2.5: Learning Analytics Dashboard  
try:
    from app.api.v1.endpoints import analytics
    api_router.include_router(analytics.router, prefix="/analytics", tags=["learning-analytics"])
    logger.info("✅ Analytics endpoints loaded")
except (ImportError, AttributeError) as e:
    logger.warning(f"⚠️ Analytics endpoints not available: {e}")

# System health monitoring
api_router.include_router(health.router, prefix="/health", tags=["health"])
