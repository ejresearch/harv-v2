"""
Health check endpoints
Essential for monitoring and deployment
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..core.database import get_db
from ..core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.version,
        "debug": settings.debug
    }

@router.get("/health/database")
async def database_health(db: Session = Depends(get_db)):
    """Database connectivity check"""
    try:
        # Simple query to test database connection
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "database": "healthy",
            "connection": "active",
            "query_result": result
        }
    except Exception as e:
        return {
            "database": "unhealthy", 
            "error": str(e),
            "status_code": 503
        }

@router.get("/health/detailed")  
async def detailed_health(db: Session = Depends(get_db)):
    """Comprehensive health check"""
    health_status = {
        "service": settings.app_name,
        "version": settings.version,
        "status": "healthy",
        "checks": {}
    }
    
    # Database check
    try:
        db.execute(text("SELECT 1")).scalar()
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # OpenAI API key check
    if settings.openai_api_key:
        health_status["checks"]["openai_key"] = "configured"
    else:
        health_status["checks"]["openai_key"] = "missing"
        health_status["status"] = "degraded"
    
    # Memory system check (placeholder for Phase 2)
    health_status["checks"]["memory_system"] = "not_implemented_yet"
    
    return health_status
