"""
Health monitoring endpoints - COMPLETE WORKING IMPLEMENTATION
Real system health checks with database connectivity testing
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import psutil
import time

from app.core.database import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check - always available"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Harv v2.0 - Intelligent Tutoring System",
        "version": "2.0.0"
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Comprehensive health check with real system metrics"""
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {},
        "system": {},
        "database": {},
        "services": {}
    }
    
    # System metrics
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status["system"] = {
            "cpu_usage_percent": round(cpu_percent, 1),
            "memory_usage_percent": round(memory.percent, 1),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_usage_percent": round(disk.percent, 1),
            "uptime_seconds": round(time.time() - psutil.boot_time(), 0)
        }
        health_status["checks"]["system_metrics"] = "healthy"
    except Exception as e:
        health_status["checks"]["system_metrics"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Database connectivity
    try:
        result = db.execute(text("SELECT 1 as test_query")).fetchone()
        if result and result[0] == 1:
            health_status["database"] = {
                "status": "connected",
                "url": settings.database_url.split("://")[0] + "://***",
                "query_test": "passed"
            }
            health_status["checks"]["database"] = "healthy"
        else:
            health_status["checks"]["database"] = "query_failed"
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["database"] = {"status": "error", "detail": str(e)}
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "degraded"
    
    # Configuration checks
    health_status["services"] = {
        "openai_configured": "yes" if settings.openai_api_key else "no",
        "jwt_configured": "yes" if settings.secret_key else "no",
        "debug_mode": settings.debug,
        "cors_origins": len(settings.cors_origins)
    }
    
    return health_status
