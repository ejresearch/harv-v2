"""
API v1 Router - Phase 2.5 Complete Integration
Includes memory, chat, WebSocket, and analytics endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, health, memory, chat, analytics

api_router = APIRouter()

# Core authentication and user management
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Phase 2: Enhanced Memory System
api_router.include_router(memory.router, prefix="/memory", tags=["enhanced-memory"])

# Phase 2.5: OpenAI Integration & Real-time Chat
api_router.include_router(chat.router, prefix="/chat", tags=["ai-tutoring"])

# Phase 2.5: Learning Analytics Dashboard
api_router.include_router(analytics.router, prefix="/analytics", tags=["learning-analytics"])

# System health monitoring
api_router.include_router(health.router, prefix="/health", tags=["health"])
