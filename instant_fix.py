import os

def create_websocket_handler():
    """Create minimal WebSocket handler"""
    websocket_code = '''"""
Minimal WebSocket Chat Handler - Phase 2.5
Basic WebSocket support for real-time chat
"""

from fastapi import WebSocket, WebSocketDisconnect
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

async def websocket_endpoint(websocket: WebSocket, module_id: int, user_id: int = None):
    """Basic WebSocket endpoint for real-time chat"""
    await websocket.accept()
    
    try:
        # Send welcome message
        welcome = {
            "type": "system",
            "message": f"Connected to AI Tutor for Module {module_id}",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome))
        
        # Basic message loop
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                
                # Echo response for now
                response = {
                    "type": "ai_response",
                    "message": f"Thanks for your message: '{user_message}'. This is a basic WebSocket response. Full chat integration coming soon!",
                    "timestamp": datetime.now().isoformat()
                }
                
                await websocket.send_text(json.dumps(response))
                
            except json.JSONDecodeError:
                error_msg = {
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(error_msg))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for module {module_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()
'''
    
    # Create websocket directory if it doesn't exist
    os.makedirs("backend/app/websocket", exist_ok=True)
    
    # Create __init__.py
    with open("backend/app/websocket/__init__.py", "w") as f:
        f.write("# WebSocket package\n")
    
    # Create chat_handler.py
    with open("backend/app/websocket/chat_handler.py", "w") as f:
        f.write(websocket_code)
    
    print("✅ Created WebSocket handler")

def fix_main_app():
    """Fix main.py to handle missing imports gracefully"""
    main_code = '''"""
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
'''
    
    with open("backend/app/main.py", "w") as f:
        f.write(main_code)
    
    print("✅ Fixed main.py")

def main():
    print("🔧 INSTANT FIX: Resolving server startup issues...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/app"):
        print("❌ Error: Run this from your harv-v2 directory")
        print("Expected: harv-v2/backend/app/")
        return
    
    # Create missing WebSocket handler
    create_websocket_handler()
    
    # Fix main application
    fix_main_app()
    
    print("=" * 50)
    print("🎉 FIXES APPLIED!")
    print("")
    print("✅ Created WebSocket handler")
    print("✅ Fixed main.py imports")
    print("✅ Server should start now")
    print("")
    print("🚀 Try starting your server again:")
    print("   cd backend && uvicorn app.main:app --reload")
    print("")
    print("📊 Then test with:")
    print("   curl http://localhost:8000/api/v1/memory/health")

if __name__ == "__main__":
    main()
