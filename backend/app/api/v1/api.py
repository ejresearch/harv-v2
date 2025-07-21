"""
API v1 Router - Complete Configuration
File: backend/app/api/v1/api.py

Includes all endpoints for Harv v2.0 Intelligent Tutoring System:
- Authentication & User Management
- Health Monitoring
- Enhanced Memory System (Phase 2)
- Live AI Chat Integration (Phase 2.5)
"""

from fastapi import APIRouter

# Import all endpoint modules
from app.api import health, auth  # Core endpoints (existing)
from app.api.v1.endpoints import memory  # Phase 2: Enhanced Memory System

# Create main API router
api_router = APIRouter()

# =============================================================================
# CORE SYSTEM ENDPOINTS
# =============================================================================

# Health monitoring endpoints
api_router.include_router(
    health.router,
    tags=["health-monitoring"],
    responses={
        200: {"description": "System healthy"},
        503: {"description": "System degraded/unhealthy"}
    }
)

# Authentication and user management
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"],
    responses={
        200: {"description": "Authentication successful"},
        401: {"description": "Authentication failed"},
        422: {"description": "Validation error"}
    }
)

# =============================================================================
# PHASE 2: ENHANCED MEMORY SYSTEM ENDPOINTS
# =============================================================================

# Enhanced 4-layer memory system
api_router.include_router(
    memory.router,
    prefix="/memory",
    tags=["enhanced-memory"],
    responses={
        200: {"description": "Memory system operational"},
        401: {"description": "Authentication required"},
        500: {"description": "Memory system error"}
    }
)

# =============================================================================
# PHASE 2.5: LIVE AI CHAT ENDPOINTS (Ready for Implementation)
# =============================================================================

# Uncomment when Phase 2.5 chat endpoints are implemented:
# from app.api.v1.endpoints import chat
# 
# api_router.include_router(
#     chat.router,
#     prefix="/chat",
#     tags=["ai-tutoring"],
#     responses={
#         200: {"description": "Chat response generated"},
#         401: {"description": "Authentication required"},
#         429: {"description": "Rate limit exceeded"},
#         500: {"description": "AI service error"}
#     }
# )

# =============================================================================
# FUTURE ENDPOINTS (Phase 3+)
# =============================================================================

# Uncomment when additional endpoints are implemented:

# Learning modules and curriculum
# from app.api.v1.endpoints import modules
# api_router.include_router(
#     modules.router,
#     prefix="/modules", 
#     tags=["learning-modules"]
# )

# User progress and analytics
# from app.api.v1.endpoints import progress
# api_router.include_router(
#     progress.router,
#     prefix="/progress",
#     tags=["learning-analytics"] 
# )

# Administrative endpoints
# from app.api.v1.endpoints import admin
# api_router.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["administration"],
#     dependencies=[Depends(require_admin_role)]
# )

# =============================================================================
# API DOCUMENTATION METADATA
# =============================================================================

# API Router metadata for OpenAPI documentation
api_router.tags_metadata = [
    {
        "name": "health-monitoring",
        "description": "System health checks and monitoring endpoints"
    },
    {
        "name": "authentication", 
        "description": "User registration, login, and JWT token management"
    },
    {
        "name": "enhanced-memory",
        "description": "4-layer memory system for personalized learning context"
    },
    {
        "name": "ai-tutoring",
        "description": "Live AI tutoring with Socratic methodology (Phase 2.5)"
    },
    {
        "name": "learning-modules",
        "description": "15 communication modules and curriculum management"
    },
    {
        "name": "learning-analytics", 
        "description": "Progress tracking and educational analytics"
    },
    {
        "name": "administration",
        "description": "Administrative functions and system management"
    }
]
