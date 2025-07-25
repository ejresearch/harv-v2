"""
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
