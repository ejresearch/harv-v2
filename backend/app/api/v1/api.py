"""
API v1 Router - Working Configuration
File: backend/app/api/v1/api.py
"""

from fastapi import APIRouter

# Import only existing endpoint modules
from app.api.v1.endpoints import memory

# Create main API router
api_router = APIRouter()

# Phase 2: Enhanced Memory System endpoints
api_router.include_router(
    memory.router, 
    prefix="/memory", 
    tags=["enhanced-memory"]
)
