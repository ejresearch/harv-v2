"""
Harv v2.0 Main Application - Phase 2.5 Complete
Enhanced Memory + OpenAI + WebSocket + Analytics Integration
"""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from app.core.config import settings
from app.core.database import engine
from app.models import user, course, memory  # Import all models
from app.api.v1.api import api_router
from app.websocket.chat_handler import websocket_endpoint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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

# WebSocket endpoint for real-time chat
@app.websocket("/api/v1/chat/ws/{module_id}")
async def websocket_chat_endpoint(websocket: WebSocket, module_id: int, user_id: int = None):
    """Real-time WebSocket chat with enhanced memory + OpenAI"""
    await websocket_endpoint(websocket, module_id, user_id)

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Harv v2.0 - AI Tutoring Platform",
        "version": "2.5.0",
        "status": "operational",
        "features": [
            "4-layer enhanced memory system",
            "OpenAI GPT-4 integration", 
            "Real-time WebSocket chat",
            "Learning analytics dashboard",
            "Socratic methodology enforcement"
        ]
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Harv v2.0 Phase 2.5 starting up...")
    logger.info("🧠 Enhanced Memory System: ACTIVE")
    logger.info("🤖 OpenAI Integration: ACTIVE") 
    logger.info("🔌 WebSocket Chat: ACTIVE")
    logger.info("📊 Analytics Dashboard: ACTIVE")
    logger.info("✅ All systems operational")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Harv v2.0 shutting down...")
    logger.info("✅ Shutdown complete")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
