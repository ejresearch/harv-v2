#!/usr/bin/env python3
"""
Quick Demo User Setup for Harv v2.0
Creates just the demo users to fix the 401 login error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.models.user import User

def setup_demo_users():
    """Setup demo users only"""
    
    print("🚀 Setting up Harv v2.0 demo users...")
    print("=====================================")
    
    # Create tables first
    create_tables()
    print("✅ Database tables ready")
    
    db = SessionLocal()
    
    try:
        # Demo users data
        users_data = [
            {
                "email": "student@demo.com", 
                "name": "Alex Student", 
                "password": "student123", 
                "role": "student"
            },
            {
                "email": "teacher@demo.com", 
                "name": "Dr. Sarah Educator", 
                "password": "teacher123", 
                "role": "educator"
            },
            {
                "email": "admin@demo.com", 
                "name": "System Administrator", 
                "password": "admin123", 
                "role": "admin"
            },
            {
                "email": "demo@harv.com", 
                "name": "Demo User (All Access)", 
                "password": "demo123", 
                "role": "universal"
            }
        ]
        
        created_count = 0
        for user_data in users_data:
            # Check if user already exists
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                # Create new user
                user = User(
                    email=user_data["email"],
                    name=user_data["name"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_active=True
                )
                
                # Add role if User model supports it
                if hasattr(user, 'role'):
                    user.role = user_data["role"]
                
                db.add(user)
                created_count += 1
                print(f"✅ Created user: {user_data['email']}")
            else:
                print(f"✅ User exists: {user_data['email']}")
        
        db.commit()
        
        print(f"\n🎉 DEMO USERS READY! ({created_count} created)")
        print("=" * 40)
        print("Demo Login Credentials:")
        print("  🎓 Student: student@demo.com / student123")
        print("  🧑‍🏫 Teacher: teacher@demo.com / teacher123")
        print("  ⚙️ Admin: admin@demo.com / admin123")
        print("  🔄 Universal: demo@harv.com / demo123")
        print("")
        print("🌐 Your backend is running at: http://localhost:8000")
        print("📚 API docs: http://localhost:8000/docs")
        print("")
        print("💡 Now try logging in with any of the demo accounts!")
        
    except Exception as e:
        print(f"❌ Error creating demo users: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    setup_demo_users()
