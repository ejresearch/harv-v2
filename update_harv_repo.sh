#!/bin/bash
# update_harv_repo.sh
# Updates existing Harv v2.0 repository with dual-perspective demo backend

echo "🔄 UPDATING HARV v2.0 REPOSITORY WITH DEMO BACKEND"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [[ ! -f "backend/app/main.py" ]]; then
    echo "❌ Error: Please run this script from your harv-v2 root directory"
    echo "   Expected structure: harv-v2/backend/app/main.py"
    exit 1
fi

echo "✅ Detected harv-v2 repository structure"
echo "📁 Current directory: $(pwd)"
echo ""

# Backup existing files
echo "💾 Creating backup of existing files..."
mkdir -p backup/$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backup/$(date +%Y%m%d_%H%M%S)"

# Backup key files that will be modified
cp backend/app/models/user.py "$BACKUP_DIR/" 2>/dev/null || echo "  Note: user.py not found (will create new)"
cp backend/app/core/security.py "$BACKUP_DIR/" 2>/dev/null || echo "  Note: security.py not found (will create new)"
cp backend/app/api/v1/endpoints/auth.py "$BACKUP_DIR/" 2>/dev/null || echo "  Note: auth.py not found (will create new)"
cp backend/app/api/v1/api.py "$BACKUP_DIR/" 2>/dev/null || echo "  Note: api.py not found (will create new)"

echo "  ✅ Backup created in $BACKUP_DIR"
echo ""

# =============================================================================
# 1. UPDATE USER MODEL WITH ROLE SUPPORT
# =============================================================================

echo "1️⃣ Updating User model with role support..."

cat > backend/app/models/user.py << 'EOF'
"""
User model with demo role switching capabilities
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    """Enhanced User model with demo role support"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Role management for demo
    role = Column(String, default="student")  # 'student', 'educator', 'admin', 'universal'
    demo_active_role = Column(String, nullable=True)  # Current demo role for 'universal' users
    previous_demo_role = Column(String, nullable=True)  # For role switching history
    
    # Onboarding and profile
    onboarding_data = Column(Text)  # JSON data from onboarding
    learning_profile = Column(Text)  # JSON learning style data
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    progress_records = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    memory_summaries = relationship("MemorySummary", back_populates="user", cascade="all, delete-orphan")
    
    def get_effective_role(self):
        """Get the role user is currently acting as (for demo switching)"""
        if self.role == "universal" and self.demo_active_role:
            return self.demo_active_role
        return self.role
    
    def can_access_role(self, target_role: str) -> bool:
        """Check if user can access a specific role"""
        if self.role == "universal":
            return True  # Universal demo users can access any role
        return self.role == target_role
    
    def switch_demo_role(self, new_role: str) -> bool:
        """Switch demo role if user has universal access"""
        if self.role != "universal":
            return False
        
        valid_roles = ["student", "educator", "admin"]
        if new_role not in valid_roles:
            return False
            
        self.previous_demo_role = self.demo_active_role or self.role
        self.demo_active_role = new_role
        return True
EOF

echo "  ✅ User model updated with role switching"

# =============================================================================
# 2. CREATE DEMO ENDPOINTS
# =============================================================================

echo "2️⃣ Creating demo endpoints..."

cat > backend/app/api/v1/endpoints/demo.py << 'EOF'
"""
Demo Role Switching Endpoints
Allows seamless switching between student/teacher/admin perspectives
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import User

router = APIRouter()

class RoleSwitchRequest(BaseModel):
    target_role: str  # 'student', 'educator', 'admin'
    maintain_session: bool = True

@router.post("/switch-role")
async def switch_demo_role(
    role_request: RoleSwitchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Switch between demo roles for comprehensive system exploration"""
    
    # Check if user has demo privileges
    if current_user.role != "universal" and current_user.email != "demo@harv.com":
        raise HTTPException(
            status_code=403,
            detail="Role switching only available for demo users"
        )
    
    valid_roles = ["student", "educator", "admin"]
    if role_request.target_role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role. Must be one of: {valid_roles}"
        )
    
    # Update user's current demo role
    current_user.demo_active_role = role_request.target_role
    db.commit()
    
    return {
        "success": True,
        "switched_to": role_request.target_role,
        "previous_role": getattr(current_user, 'previous_demo_role', 'student'),
        "message": f"Demo role switched to {role_request.target_role}. You now have access to {role_request.target_role} features."
    }

@router.get("/context/{role}")
async def get_role_demo_context(role: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get demo context and sample data for specific role"""
    
    contexts = {
        "student": {
            "dashboard_features": [
                "Learning progress tracking",
                "Socratic AI chat interface", 
                "Module completion status",
                "Memory system visualization",
                "Personal learning analytics"
            ],
            "sample_data": {
                "active_modules": 5,
                "completion_rate": "65%",
                "chat_sessions": 12,
                "learning_insights": 8
            }
        },
        "educator": {
            "dashboard_features": [
                "Student progress monitoring",
                "Module content management",
                "Socratic prompt configuration",
                "Learning analytics dashboard",
                "Content creation tools"
            ],
            "sample_data": {
                "total_students": 24,
                "active_modules": 15,
                "avg_engagement": "87%",
                "memory_insights": 156
            }
        },
        "admin": {
            "dashboard_features": [
                "System performance monitoring",
                "User management interface",
                "Database health tracking", 
                "Memory system analytics",
                "Configuration management"
            ],
            "sample_data": {
                "system_uptime": "99.9%",
                "total_users": 342,
                "api_response_time": "67ms",
                "memory_efficiency": "94%"
            }
        }
    }
    
    if role not in contexts:
        raise HTTPException(status_code=404, detail="Role context not found")
    
    return contexts[role]

@router.get("/available-features")
async def get_available_demo_features(current_user: User = Depends(get_current_user)):
    """Get all available features based on current demo role"""
    
    current_role = getattr(current_user, 'demo_active_role', current_user.role)
    
    feature_matrix = {
        "student": {
            "dashboard": "Student learning dashboard",
            "chat": "Socratic AI tutoring chat",
            "modules": "Learning module access",
            "progress": "Personal progress tracking",
            "memory": "Memory system visualization"
        },
        "educator": {
            "dashboard": "Educator analytics dashboard", 
            "students": "Student progress monitoring",
            "content": "Module content management",
            "analytics": "Learning effectiveness analytics",
            "prompts": "Socratic prompt configuration"
        },
        "admin": {
            "dashboard": "System administration dashboard",
            "users": "User account management", 
            "health": "System health monitoring",
            "database": "Database activity tracking",
            "config": "System configuration management"
        }
    }
    
    return {
        "current_role": current_role,
        "available_features": feature_matrix.get(current_role, {}),
        "can_switch_roles": current_user.role == "universal",
        "demo_mode": True
    }
EOF

echo "  ✅ Demo endpoints created"

# =============================================================================
# 3. UPDATE API ROUTER TO INCLUDE DEMO
# =============================================================================

echo "3️⃣ Updating API router..."

# Check if api.py exists and update it
if [[ -f "backend/app/api/v1/api.py" ]]; then
    # Add demo import and router if not already present
    if ! grep -q "from.*demo" backend/app/api/v1/api.py; then
        # Add demo import
        sed -i '/from app\.api\.v1\.endpoints import/s/)/, demo)/' backend/app/api/v1/api.py
        
        # Add demo router include
        echo 'api_router.include_router(demo.router, prefix="/demo", tags=["demo-features"])' >> backend/app/api/v1/api.py
        
        echo "  ✅ Demo router added to existing API"
    else
        echo "  ✅ Demo router already included"
    fi
else
    # Create new api.py with demo included
    cat > backend/app/api/v1/api.py << 'EOF'
"""
API router with demo endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, health, memory, chat, modules, 
    progress, onboarding, admin, demo
)

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(memory.router, prefix="/memory", tags=["enhanced-memory"])
api_router.include_router(chat.router, prefix="/chat", tags=["ai-chat"])
api_router.include_router(modules.router, prefix="/modules", tags=["learning-modules"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress-tracking"])
api_router.include_router(onboarding.router, prefix="/onboarding", tags=["user-onboarding"])
api_router.include_router(admin.router, prefix="/admin", tags=["administration"])
api_router.include_router(demo.router, prefix="/demo", tags=["demo-features"])
EOF
    echo "  ✅ New API router created with demo endpoints"
fi

# =============================================================================
# 4. CREATE DEMO DATA SETUP SCRIPT
# =============================================================================

echo "4️⃣ Creating demo data setup script..."

cat > backend/setup_demo_data.py << 'EOF'
#!/usr/bin/env python3
"""
Quick Demo Data Setup for Harv v2.0
Creates demo users and sample data
"""

import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.models import Module, User, Conversation, Message, UserProgress
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import json

async def setup_demo_data():
    """Setup demo data quickly"""
    
    print("🚀 Setting up Harv v2.0 demo data...")
    
    create_tables()
    db = SessionLocal()
    
    try:
        # Create demo users
        users_data = [
            {"email": "student@demo.com", "name": "Alex Student", "password": "student123", "role": "student"},
            {"email": "teacher@demo.com", "name": "Dr. Sarah Educator", "password": "teacher123", "role": "educator"},
            {"email": "admin@demo.com", "name": "System Administrator", "password": "admin123", "role": "admin"},
            {"email": "demo@harv.com", "name": "Demo User (All Access)", "password": "demo123", "role": "universal"}
        ]
        
        created_users = []
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    email=user_data["email"],
                    name=user_data["name"],
                    hashed_password=get_password_hash(user_data["password"]),
                    role=user_data["role"],
                    is_active=True
                )
                db.add(user)
                created_users.append(user)
        
        db.flush()
        print(f"✅ Created {len(created_users)} demo users")
        
        # Create sample modules
        modules_data = [
            {"id": 1, "title": "Your Four Worlds", "description": "Communication models and perception"},
            {"id": 2, "title": "Writing: Persistence of Words", "description": "How writing transformed communication"},
            {"id": 3, "title": "Books: Mass Communication", "description": "The printing press revolution"},
        ]
        
        created_modules = []
        for mod_data in modules_data:
            existing = db.query(Module).filter(Module.id == mod_data["id"]).first()
            if not existing:
                module = Module(
                    title=mod_data["title"],
                    description=mod_data["description"],
                    system_prompt="Guide students through Socratic discovery.",
                    module_prompt="Help students explore communication concepts.",
                    learning_objectives="Understand key communication principles.",
                    difficulty_level="intermediate",
                    estimated_duration=45,
                    is_active=True
                )
                db.add(module)
                created_modules.append(module)
        
        db.flush()
        print(f"✅ Created {len(created_modules)} sample modules")
        
        # Create sample conversations
        student_user = db.query(User).filter(User.role == "student").first()
        if student_user:
            conversation = Conversation(
                user_id=student_user.id,
                module_id=1,
                title="Learning Session 1",
                memory_summary="Student explored communication concepts",
                current_grade="progressing"
            )
            db.add(conversation)
            db.flush()
            
            # Add sample messages
            messages = [
                {"role": "user", "content": "What is communication theory?"},
                {"role": "assistant", "content": "Great question! Instead of me telling you, what do you think happens when two people try to share an idea?"}
            ]
            
            for msg in messages:
                message = Message(
                    conversation_id=conversation.id,
                    role=msg["role"],
                    content=msg["content"],
                    user_id=student_user.id if msg["role"] == "user" else None
                )
                db.add(message)
            
            print("✅ Created sample conversation")
        
        db.commit()
        
        print("\n🎉 DEMO SETUP COMPLETE!")
        print("=" * 40)
        print("Demo Accounts:")
        print("  🎓 Student: student@demo.com / student123")
        print("  🧑‍🏫 Teacher: teacher@demo.com / teacher123")
        print("  ⚙️ Admin: admin@demo.com / admin123")
        print("  🔄 Universal: demo@harv.com / demo123")
        print("\nStart server: uvicorn app.main:app --reload")
        print("API Docs: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(setup_demo_data())
EOF

chmod +x backend/setup_demo_data.py
echo "  ✅ Demo data setup script created"

# =============================================================================
# 5. UPDATE MAIN APP TO SHOW DEMO INFO
# =============================================================================

echo "5️⃣ Updating main app with demo information..."

# Check if main.py exists and add demo info to root endpoint
if [[ -f "backend/app/main.py" ]]; then
    # Add demo info to existing root endpoint if not already present
    if ! grep -q "demo_accounts" backend/app/main.py; then
        # Create a backup and update
        cp backend/app/main.py backend/app/main.py.backup
        
        # Update the root endpoint to include demo info
        cat > temp_main_update.py << 'EOF'
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.version,
        "status": "🚀 FULLY OPERATIONAL",
        "demo_mode": "🎯 DUAL PERSPECTIVE DEMO ACTIVE",
        "demo_accounts": {
            "student": "student@demo.com / student123",
            "educator": "teacher@demo.com / teacher123", 
            "admin": "admin@demo.com / admin123",
            "universal": "demo@harv.com / demo123 (role switching enabled)"
        },
        "features": {
            "enhanced_memory": "✅ ACTIVE - 4-layer memory system",
            "socratic_chat": "✅ ACTIVE - AI tutoring with questioning",
            "learning_modules": "✅ ACTIVE - 15 communication modules",
            "role_switching": "✅ ACTIVE - Seamless perspective switching",
            "real_time_metrics": "✅ ACTIVE - Performance monitoring"
        },
        "api_endpoints": {
            "documentation": "/docs",
            "health_check": "/api/v1/health/",
            "demo_switch_role": "/api/v1/demo/switch-role",
            "modules": "/api/v1/modules/",
            "memory": "/api/v1/memory/enhanced/1",
            "chat": "/api/v1/chat/enhanced"
        }
    }
EOF
        
        # Replace the root endpoint in main.py
        python3 -c "
import re
with open('backend/app/main.py', 'r') as f:
    content = f.read()

# Replace the root endpoint
new_root = open('temp_main_update.py', 'r').read()
pattern = r'@app\.get\(\"/\"\).*?return \{.*?\}'
content = re.sub(pattern, new_root, content, flags=re.DOTALL)

with open('backend/app/main.py', 'w') as f:
    f.write(content)
"
        rm temp_main_update.py
        echo "  ✅ Main app updated with demo information"
    else
        echo "  ✅ Demo information already present in main app"
    fi
fi

# =============================================================================
# 6. CREATE QUICK START SCRIPT
# =============================================================================

echo "6️⃣ Creating quick start script..."

cat > start_demo.sh << 'EOF'
#!/bin/bash
# Quick start script for Harv v2.0 demo

echo "🚀 Starting Harv v2.0 Dual-Perspective Demo"
echo "========================================"

# Navigate to backend
cd backend

# Setup demo data
echo "📊 Setting up demo data..."
python setup_demo_data.py

echo ""
echo "🌐 Starting server..."
echo "Demo will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x start_demo.sh
echo "  ✅ Quick start script created"

# =============================================================================
# COMPLETION MESSAGE
# =============================================================================

echo ""
echo "🎉 HARV v2.0 REPOSITORY UPDATE COMPLETE!"
echo "========================================"
echo ""
echo "📋 What was updated:"
echo "  ✅ User model with role switching support"
echo "  ✅ Demo API endpoints for role switching"
echo "  ✅ Updated API router with demo endpoints"
echo "  ✅ Demo data setup script"
echo "  ✅ Enhanced main app with demo info"
echo "  ✅ Quick start script"
echo ""
echo "🚀 To start the demo:"
echo "  ./start_demo.sh"
echo ""
echo "🎯 Demo accounts will be:"
echo "  🎓 Student: student@demo.com / student123"
echo "  🧑‍🏫 Teacher: teacher@demo.com / teacher123"
echo "  ⚙️ Admin: admin@demo.com / admin123"
echo "  🔄 Universal: demo@harv.com / demo123 (can switch roles)"
echo ""
echo "💾 Backup of original files saved in: $BACKUP_DIR"
echo ""
echo "Ready to demo both student AND teacher perspectives! 🎉"
