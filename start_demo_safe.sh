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
