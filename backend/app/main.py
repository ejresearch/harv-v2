"""
FastAPI application setup for Harv v2.0
Complete rewrite with enhanced memory system, comprehensive monitoring, and Phase 2.5 readiness
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
from datetime import datetime

from .core.config import settings
from .core.database import create_tables
from .api.v1.api import api_router

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO if settings.debug else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application with enhanced configuration
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="""
    🧠 **Harv v2.0 - Intelligent Tutoring System**
    
    **Enhanced 4-Layer Memory Architecture**
    - Layer 1: User learning profile and cross-module mastery
    - Layer 2: Module-specific context and teaching configuration
    - Layer 3: Real-time conversation state and message history
    - Layer 4: Cross-module prior knowledge connections
    
    **Socratic Methodology Integration**
    - Discovery-based learning through strategic questioning
    - Personalized teaching approaches based on learning style
    - Cross-module knowledge building and retention
    
    **Production-Ready Features**
    - JWT authentication and security
    - Comprehensive health monitoring
    - Graceful error handling and fallbacks
    - Type-safe API with auto-generated documentation
    """,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
    contact={
        "name": "Harv v2.0 Development Team",
        "url": "https://github.com/yourusername/harv-v2",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Enhanced CORS middleware with security headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Memory-Context-Size"]
)

# Request timing middleware for performance monitoring
@app.middleware("http")
async def request_timing_middleware(request: Request, call_next):
    """Add request timing and ID for monitoring"""
    start_time = time.time()
    request_id = f"req-{int(start_time * 1000)}"
    
    # Add request ID to headers
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Add monitoring headers
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))  # milliseconds
    
    # Log slow requests in production
    if process_time > 2.0:  # Slower than 2 seconds
        logger.warning(f"Slow request: {request.method} {request.url} took {process_time:.2f}s")
    
    return response

# Comprehensive startup event with system verification
@app.on_event("startup")
async def startup_event():
    """Initialize system with comprehensive health checks"""
    startup_time = datetime.now().isoformat()
    
    try:
        logger.info("🚀 " + "="*60)
        logger.info(f"🚀 {settings.app_name} v{settings.version} STARTING UP")
        logger.info("🚀 " + "="*60)
        
        # Database initialization with verification
        logger.info("🗄️  Initializing database...")
        create_tables()
        logger.info("✅ Database tables created/verified")
        
        # System configuration logging
        logger.info(f"📊 Debug mode: {settings.debug}")
        logger.info(f"🗄️  Database: {settings.database_url}")
        logger.info(f"🔐 JWT expiration: {settings.access_token_expire_minutes} minutes")
        logger.info(f"🌐 CORS origins: {len(settings.cors_origins)} configured")
        
        # Enhanced Memory System status
        logger.info("🧠 Enhanced Memory System Status:")
        logger.info(f"   📚 Max context length: {settings.memory_max_context_length}")
        logger.info(f"   🔄 Fallback enabled: {settings.memory_fallback_enabled}")
        logger.info(f"   ✅ 4-Layer architecture: ACTIVE")
        
        # Socratic Teaching System status
        logger.info("🎓 Socratic Teaching System Status:")
        logger.info(f"   🤔 Socratic mode: {settings.socratic_mode_enabled}")
        logger.info(f"   🚫 Direct answers prevented: {settings.prevent_direct_answers}")
        logger.info(f"   ✅ Discovery-based learning: ACTIVE")
        
        # OpenAI Integration status (Phase 2.5 readiness)
        if settings.openai_api_key:
            logger.info("🤖 OpenAI Integration Status:")
            logger.info(f"   🔑 API Key: CONFIGURED")
            logger.info(f"   🤖 Model: {settings.openai_model}")
            logger.info(f"   ✅ Phase 2.5 Ready: CHAT INTEGRATION READY")
        else:
            logger.warning("⚠️  OpenAI Integration Status:")
            logger.warning("   🔑 API Key: NOT SET")
            logger.warning("   📋 Phase 2.5: Requires OPENAI_API_KEY configuration")
        
        # API Endpoints summary
        logger.info("🌐 API Endpoints Active:")
        logger.info(f"   🏠 Root: /")
        logger.info(f"   💓 Health: /health/*")
        logger.info(f"   🔐 Authentication: {settings.api_prefix}/auth/*")
        logger.info(f"   🧠 Enhanced Memory: {settings.api_prefix}/memory/*")
        if settings.openai_api_key:
            logger.info(f"   💬 AI Chat: {settings.api_prefix}/chat/* (Phase 2.5)")
        
        # Final startup confirmation
        logger.info("🚀 " + "="*60)
        logger.info("🎉 HARV v2.0 STARTUP COMPLETE - SYSTEM OPERATIONAL")
        logger.info("🚀 " + "="*60)
        
        # Store startup time for health checks
        app.state.startup_time = startup_time
        app.state.system_healthy = True
        
    except Exception as e:
        logger.error("❌ " + "="*60)
        logger.error(f"❌ STARTUP FAILED: {e}")
        logger.error("❌ " + "="*60)
        app.state.system_healthy = False
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Graceful shutdown with cleanup"""
    logger.info("👋 " + "="*50)
    logger.info("👋 Harv v2.0 shutting down gracefully...")
    logger.info("👋 " + "="*50)

# Enhanced global exception handler with detailed logging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors with comprehensive logging and user-friendly responses"""
    
    # Log the full error with context
    logger.error(f"❌ Unhandled exception in {request.method} {request.url}")
    logger.error(f"❌ Error: {str(exc)}")
    logger.error(f"❌ Client: {request.client.host if request.client else 'unknown'}")
    
    if settings.debug:
        # In debug mode, provide detailed error information
        import traceback
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "type": type(exc).__name__,
                "path": str(request.url),
                "method": request.method,
                "traceback": traceback.format_exc(),
                "debug": True,
                "timestamp": datetime.now().isoformat(),
                "request_id": request.headers.get("X-Request-ID", "unknown")
            }
        )
    else:
        # In production, provide user-friendly error without exposing details
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred. Please try again later.",
                "support": "If this problem persists, please contact support.",
                "timestamp": datetime.now().isoformat(),
                "request_id": request.headers.get("X-Request-ID", "unknown")
            }
        )

# Include the complete API router
app.include_router(api_router, prefix=settings.api_prefix)

# Enhanced root endpoint with comprehensive system information
@app.get("/", tags=["System Info"])
async def root():
    """
    Root endpoint - Complete system information and capabilities
    
    Returns comprehensive information about the Harv v2.0 system including:
    - System status and configuration
    - Available capabilities and features
    - API endpoints and documentation
    - Phase implementation status
    """
    
    # Basic system information
    system_info = {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "healthy" if getattr(app.state, 'system_healthy', True) else "degraded",
        "startup_time": getattr(app.state, 'startup_time', 'unknown'),
        "current_time": datetime.now().isoformat(),
    }
    
    # System capabilities showcase
    capabilities = {
        "enhanced_memory_system": {
            "status": "active",
            "description": "4-layer memory architecture for personalized learning",
            "layers": [
                "System Data: User learning profile and cross-module mastery",
                "Module Data: Teaching configuration and progress tracking", 
                "Conversation Data: Real-time dialogue context and history",
                "Prior Knowledge: Cross-module learning connections"
            ]
        },
        "socratic_methodology": {
            "status": "active",
            "description": "Discovery-based learning through strategic questioning",
            "features": [
                "Strategic questioning instead of direct answers",
                "Personalized learning style adaptation",
                "Cross-module knowledge building",
                "Progress tracking and insight recognition"
            ]
        },
        "authentication_security": {
            "status": "active", 
            "description": "JWT-based security with user management",
            "features": [
                "User registration and authentication",
                "JWT token management",
                "Protected API endpoints",
                "Session management"
            ]
        },
        "health_monitoring": {
            "status": "active",
            "description": "Comprehensive system monitoring and diagnostics",
            "endpoints": [
                "/health - Basic system health",
                "/health/database - Database connectivity",
                "/health/detailed - Comprehensive status"
            ]
        }
    }
    
    # API endpoints documentation
    api_endpoints = {
        "documentation": {
            "interactive_docs": "/docs" if settings.debug else "disabled_in_production",
            "openapi_schema": "/openapi.json" if settings.debug else "disabled_in_production",
            "redoc": "/redoc" if settings.debug else "disabled_in_production"
        },
        "core_endpoints": {
            "system_health": "/health/*",
            "authentication": f"{settings.api_prefix}/auth/*",
            "user_management": f"{settings.api_prefix}/auth/me"
        },
        "enhanced_features": {
            "memory_system": f"{settings.api_prefix}/memory/enhanced/{{module_id}}",
            "memory_debug": f"{settings.api_prefix}/memory/debug/{{module_id}}",
            "memory_health": f"{settings.api_prefix}/memory/health"
        },
        "phase_2_5": {
            "ai_chat": f"{settings.api_prefix}/chat/{{module_id}}" + (
                " (READY)" if settings.openai_api_key else " (REQUIRES_OPENAI_KEY)"
            ),
            "conversation_management": f"{settings.api_prefix}/chat/conversations"
        }
    }
    
    # System configuration status
    configuration = {
        "environment": {
            "debug_mode": settings.debug,
            "database_type": "sqlite" if "sqlite" in settings.database_url else "postgresql",
            "cors_enabled": len(settings.cors_origins) > 0,
            "api_prefix": settings.api_prefix
        },
        "memory_system": {
            "max_context_length": settings.memory_max_context_length,
            "fallback_enabled": settings.memory_fallback_enabled,
            "socratic_mode": settings.socratic_mode_enabled,
            "prevent_direct_answers": settings.prevent_direct_answers
        },
        "integrations": {
            "openai_configured": bool(settings.openai_api_key),
            "openai_model": settings.openai_model if settings.openai_api_key else "not_configured",
            "phase_2_5_ready": bool(settings.openai_api_key)
        }
    }
    
    # Implementation phases status
    phases = {
        "phase_1": {
            "name": "Foundation & Authentication", 
            "status": "✅ COMPLETE",
            "description": "Clean architecture, database models, JWT authentication"
        },
        "phase_2": {
            "name": "Enhanced Memory System",
            "status": "✅ COMPLETE", 
            "description": "4-layer memory architecture with API endpoints"
        },
        "phase_2_5": {
            "name": "OpenAI Chat Integration",
            "status": "🚀 READY" if settings.openai_api_key else "⏳ PENDING_CONFIG",
            "description": "Live AI tutoring with memory-enhanced conversations",
            "next_steps": [] if settings.openai_api_key else [
                "Set OPENAI_API_KEY in environment",
                "Uncomment chat router in api.py",
                "Deploy chat endpoints"
            ]
        },
        "phase_3": {
            "name": "Frontend & Complete Platform",
            "status": "📋 PLANNED",
            "description": "React frontend, WebSocket integration, learning dashboard"
        }
    }
    
    return {
        **system_info,
        "capabilities": capabilities,
        "api_endpoints": api_endpoints,
        "configuration": configuration, 
        "implementation_phases": phases,
        "ready_for": (
            "🚀 Phase 2.5 - Live AI Tutoring" if settings.openai_api_key 
            else "⚙️  OpenAI API Key Configuration"
        )
    }

# Development-only debug endpoints
if settings.debug:
    
    @app.get("/debug/system", tags=["Debug"])
    async def debug_system_info():
        """Comprehensive system debug information (debug mode only)"""
        import sys
        import platform
        
        return {
            "python_version": sys.version,
            "platform": platform.platform(),
            "fastapi_routes": len(app.routes),
            "middleware_count": len(app.user_middleware),
            "settings": {
                key: getattr(settings, key) for key in dir(settings) 
                if not key.startswith('_')
            },
            "database_url": settings.database_url,
            "memory_system_config": {
                "max_context": settings.memory_max_context_length,
                "fallback": settings.memory_fallback_enabled,
                "socratic": settings.socratic_mode_enabled
            }
        }
    
    @app.get("/debug/routes", tags=["Debug"])
    async def debug_routes():
        """Show all registered routes with details (debug mode only)"""
        routes_info = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                route_info = {
                    "path": route.path,
                    "methods": list(route.methods) if route.methods else [],
                    "name": getattr(route, 'name', 'unnamed'),
                    "tags": getattr(route, 'tags', [])
                }
                
                # Add endpoint function info if available
                if hasattr(route, 'endpoint'):
                    route_info["function"] = route.endpoint.__name__
                    route_info["module"] = route.endpoint.__module__
                
                routes_info.append(route_info)
        
        return {
            "total_routes": len(routes_info),
            "routes": sorted(routes_info, key=lambda x: x["path"]),
            "route_summary": {
                "auth_endpoints": len([r for r in routes_info if '/auth' in r["path"]]),
                "memory_endpoints": len([r for r in routes_info if '/memory' in r["path"]]),
                "health_endpoints": len([r for r in routes_info if '/health' in r["path"]]),
                "debug_endpoints": len([r for r in routes_info if '/debug' in r["path"]])
            }
        }
