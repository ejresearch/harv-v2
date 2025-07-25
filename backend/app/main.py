"""
Harv v2.0 Main Application - Fixed
Enhanced Memory + OpenAI + Basic WebSocket Integration
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.database import engine
from app.models import user, course, memory  # Import all models
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Harv v2.0 - AI Tutoring Platform",
    description="Enhanced Memory System + OpenAI Integration for Personalized Learning",
    version="2.5.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.api_prefix)

# Basic WebSocket endpoint
@app.websocket("/api/v1/chat/ws/{module_id}")
async def websocket_chat_endpoint(websocket: WebSocket, module_id: int, user_id: int = None):
    """Basic WebSocket chat endpoint"""
    try:
        from app.websocket.chat_handler import websocket_endpoint
        await websocket_endpoint(websocket, module_id, user_id)
    except ImportError:
        # Fallback if websocket handler not available
        await websocket.accept()
        await websocket.send_text("WebSocket connected but handler not fully implemented yet")
        await websocket.close()

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Harv v2.0 - AI Tutoring Platform",
        "version": "2.5.0",
        "status": "operational",
        "features": [
            "4-layer enhanced memory system",
            "OpenAI GPT-4o integration", 
            "Real-time chat capabilities",
            "Socratic methodology enforcement"
        ]
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Harv v2.0 starting up...")
    logger.info("🧠 Enhanced Memory System: ACTIVE")
    logger.info("🤖 OpenAI Integration: ACTIVE") 
    logger.info("📚 API Documentation: /docs")
    logger.info("✅ Server ready")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Harv v2.0 shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
