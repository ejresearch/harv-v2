"""
API v1 Router - Complete with all endpoints
"""

from fastapi import APIRouter

# Import all available endpoints
from app.api.v1.endpoints import auth, users, health, memory

api_router = APIRouter()

# Authentication
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# User management  
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Phase 2: Enhanced Memory System
api_router.include_router(memory.router, prefix="/memory", tags=["enhanced-memory"])

# System health monitoring
api_router.include_router(health.router, prefix="/health", tags=["health"])
