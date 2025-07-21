"""
Demo Data API Endpoints
File: backend/app/api/v1/endpoints/demo.py
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import json

from app.core.database import get_db

router = APIRouter()

@router.get("/stats")
async def get_demo_stats(db: Session = Depends(get_db)):
    """Get real database statistics for demo"""
    try:
        # Get real counts from database
        users_count = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        conversations_count = db.execute(text("SELECT COUNT(*) FROM conversations")).scalar() or 0
        messages_count = db.execute(text("SELECT COUNT(*) FROM messages")).scalar() or 0
        memories_count = db.execute(text("SELECT COUNT(*) FROM memory_summaries")).scalar() or 0
        
        return {
            "database_metrics": {
                "users": users_count,
                "conversations": conversations_count,
                "messages": messages_count,
                "memories": memories_count
            },
            "timestamp": datetime.now().isoformat(),
            "status": "real_data"
        }
    except Exception as e:
        # Fallback demo data
        return {
            "database_metrics": {
                "users": 1,
                "conversations": 0,
                "messages": 0,
                "memories": 0
            },
            "timestamp": datetime.now().isoformat(),
            "status": f"fallback_data: {str(e)}"
        }

@router.get("/sql-activity")
async def get_sql_activity(db: Session = Depends(get_db)):
    """Get recent database activity"""
    try:
        # Get recent data from key tables
        users = db.execute(text("SELECT id, name, email FROM users LIMIT 5")).fetchall()
        conversations = db.execute(text("SELECT id, title, updated_at FROM conversations ORDER BY updated_at DESC LIMIT 3")).fetchall()
        
        return {
            "users_table": [
                {"id": row[0], "name": row[1], "email": row[2]}
                for row in users
            ],
            "conversations_table": [
                {"id": row[0], "title": row[1], "updated_at": str(row[2])}
                for row in conversations
            ],
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "users_table": [],
            "conversations_table": [],
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/create-demo-data") 
async def create_demo_data(db: Session = Depends(get_db)):
    """Create demo data for testing"""
    try:
        # This would create demo data in a real implementation
        # For now, just return success
        return {
            "message": "Demo data creation endpoint",
            "status": "not_implemented", 
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
