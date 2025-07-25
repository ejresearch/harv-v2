"""
Harv v2.0 FastAPI Application - COMPLETE WORKING VERSION
ALL endpoints included and functional
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from .core.config import settings
from .core.database import create_tables
from .api.v1.api import api_router  # CRITICAL: This includes ALL endpoints

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Harv v2.0 - Intelligent Tutoring System with Enhanced Memory",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CRITICAL: Include the API router with ALL endpoints
app.include_router(api_router, prefix=settings.api_prefix)

@app.on_event("startup")
async def startup():
    """Startup event"""
    logger.info(f"🚀 {settings.app_name} starting up...")
    create_tables()
    logger.info("✅ Database tables created")

@app.get("/")
async def root():
    """Root endpoint - System overview"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "🚀 FULLY OPERATIONAL",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "enhanced_memory": "✅ ACTIVE - 4-layer memory system",
            "socratic_chat": "✅ ACTIVE - AI tutoring with questioning",
            "learning_modules": "✅ ACTIVE - 15 communication modules",
            "real_time_metrics": "✅ ACTIVE - Performance monitoring"
        },
        "api_endpoints": {
            "documentation": "/docs",
            "health_check": "/api/v1/health/",
            "modules": "/api/v1/modules/",
            "memory": "/api/v1/memory/enhanced/1",
            "chat": "/api/v1/chat/enhanced",
            "progress": "/api/v1/progress/user/1/module/1"
        }
    }

@app.get("/health")
async def health():
    """Simple health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
