#!/bin/bash
# final_fix.sh - Fix database schema and import issues

echo "🔧 FINAL HARV v2.0 FIX - DATABASE MIGRATION"
echo "==========================================="

# 1. Fix the API router import issue
echo "1️⃣ Fixing API router imports..."

cat > backend/app/api/v1/api.py << 'EOF'
"""
Complete API Router - ALL ENDPOINTS INCLUDED
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    health,
    memory,
    chat,
    modules,
    progress,
    onboarding,
    admin
)

# Try to import demo, but don't fail if it doesn't exist
try:
    from app.api.v1.endpoints import demo
    DEMO_AVAILABLE = True
except ImportError:
    DEMO_AVAILABLE = False

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

# Include demo router only if available
if DEMO_AVAILABLE:
    api_router.include_router(demo.router, prefix="/demo", tags=["demo-features"])
EOF

echo "  ✅ Fixed API router imports"

# 2. Create database migration script
echo "2️⃣ Creating database migration script..."

cat > backend/migrate_database.py << 'EOF'
#!/usr/bin/env python3
"""
Database Migration Script
Adds role columns to existing database
"""

import sqlite3
import os
from pathlib import Path

def migrate_database():
    """Add role columns to existing users table"""
    
    db_path = Path("harv_v2.db")
    if not db_path.exists():
        print("✅ No existing database found - will create fresh")
        return
    
    print("🗄️ Migrating existing database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if role column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'role' not in columns:
            print("  ➕ Adding 'role' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'student'")
        else:
            print("  ✅ 'role' column already exists")
            
        if 'demo_active_role' not in columns:
            print("  ➕ Adding 'demo_active_role' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN demo_active_role TEXT")
        else:
            print("  ✅ 'demo_active_role' column already exists")
            
        if 'previous_demo_role' not in columns:
            print("  ➕ Adding 'previous_demo_role' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN previous_demo_role TEXT")
        else:
            print("  ✅ 'previous_demo_role' column already exists")
            
        if 'onboarding_data' not in columns:
            print("  ➕ Adding 'onboarding_data' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN onboarding_data TEXT")
        else:
            print("  ✅ 'onboarding_data' column already exists")
            
        if 'learning_profile' not in columns:
            print("  ➕ Adding 'learning_profile' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN learning_profile TEXT")
        else:
            print("  ✅ 'learning_profile' column already exists")
        
        conn.commit()
        print("  ✅ Database migration completed successfully")
        
    except Exception as e:
        print(f"  ❌ Migration error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
EOF

chmod +x backend/migrate_database.py
echo "  ✅ Migration script created"

# 3. Create a simplified startup script that handles migration
echo "3️⃣ Creating safe startup script..."

cat > start_demo_safe.sh << 'EOF'
#!/bin/bash
# Safe demo startup with database migration

echo "🚀 Starting Harv v2.0 Demo (Safe Mode)"
echo "====================================="

cd backend

# Step 1: Migrate existing database
echo "📊 Migrating database schema..."
python migrate_database.py

# Step 2: Create demo users (safe version)
echo "👥 Setting up demo users..."
python -c "
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User

# Create tables first
create_tables()

db = SessionLocal()
try:
    # Create demo users
    users_data = [
        {'email': 'student@demo.com', 'name': 'Alex Student', 'password': 'student123', 'role': 'student'},
        {'email': 'teacher@demo.com', 'name': 'Dr. Sarah Educator', 'password': 'teacher123', 'role': 'educator'},
        {'email': 'admin@demo.com', 'name': 'System Administrator', 'password': 'admin123', 'role': 'admin'},
        {'email': 'demo@harv.com', 'name': 'Demo User (All Access)', 'password': 'demo123', 'role': 'universal'}
    ]
    
    created = 0
    for user_data in users_data:
        existing = db.query(User).filter(User.email == user_data['email']).first()
        if not existing:
            user = User(
                email=user_data['email'],
                name=user_data['name'],
                hashed_password=get_password_hash(user_data['password']),
                role=user_data['role'],
                is_active=True
            )
            db.add(user)
            created += 1
    
    db.commit()
    print(f'✅ Created {created} demo users')
    
    print()
    print('🎉 DEMO USERS READY!')
    print('  🎓 Student: student@demo.com / student123')
    print('  🧑‍🏫 Teacher: teacher@demo.com / teacher123')
    print('  ⚙️ Admin: admin@demo.com / admin123')
    print('  🔄 Universal: demo@harv.com / demo123')
    
except Exception as e:
    print(f'❌ Error: {e}')
    db.rollback()
finally:
    db.close()
"

echo ""
echo "🌐 Starting server..."
echo "Demo will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x start_demo_safe.sh
echo "  ✅ Safe startup script created"

# 4. Test if existing database needs migration
echo "4️⃣ Testing database migration..."
cd backend
python migrate_database.py
cd ..

echo ""
echo "🎉 FINAL FIX COMPLETE!"
echo "====================="
echo ""
echo "🚀 Start the demo with:"
echo "  ./start_demo_safe.sh"
echo ""
echo "This script will:"
echo "  ✅ Migrate your existing database safely"
echo "  ✅ Create demo users without conflicts"
echo "  ✅ Start the server with all features"
echo ""
echo "🎯 Demo accounts:"
echo "  🎓 Student: student@demo.com / student123"
echo "  🧑‍🏫 Teacher: teacher@demo.com / teacher123"
echo "  ⚙️ Admin: admin@demo.com / admin123"
echo "  🔄 Universal: demo@harv.com / demo123"
