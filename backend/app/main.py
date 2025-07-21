"""
FastAPI application setup for Harv v2.0
Clean, production-ready application structure
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .core.config import settings
from .core.database import create_tables
from .api import auth, health

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Intelligent tutoring system with enhanced 4-layer memory architecture",
    docs_url="/docs" if settings.debug else None,  # Disable docs in production
    redoc_url="/redoc" if settings.debug else None,
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database and perform startup tasks"""
    create_tables()
    print(f"🚀 {settings.app_name} v{settings.version} starting up...")
    print(f"📊 Debug mode: {settings.debug}")
    print(f"🗄️  Database: {settings.database_url}")

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected errors gracefully"""
    if settings.debug:
        # In debug mode, show the actual error
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "detail": str(exc),
                "debug": True
            }
        )
    else:
        # In production, hide error details
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred"
            }
        )

# Include API routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["Authentication"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "healthy",
        "docs": "/docs" if settings.debug else "Documentation disabled in production"
    }
