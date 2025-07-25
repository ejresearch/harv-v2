#!/usr/bin/env python3
"""
Simple Demo Data Setup for Harv v2.0
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, create_tables
from app.core.security import get_password_hash

# Import only what we need
from app.models.user import User
from app.models.course import Module

async def setup_demo_data():
    """Setup basic demo data"""
    
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
        
        created_users = 0
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
                created_users += 1
        
        db.flush()
        print(f"✅ Created {created_users} demo users")
        
        # Create basic modules
        basic_modules = [
            {"title": "Your Four Worlds", "description": "Communication models and perception"},
            {"title": "Writing: Persistence of Words", "description": "How writing transformed communication"},
            {"title": "Books: Mass Communication", "description": "The printing press revolution"},
        ]
        
        created_modules = 0
        for i, mod_data in enumerate(basic_modules, 1):
            existing = db.query(Module).filter(Module.title == mod_data["title"]).first()
            if not existing:
                module = Module(
                    title=mod_data["title"],
                    description=mod_data["description"],
                    system_prompt="Guide students through Socratic discovery of communication concepts.",
                    module_prompt="Help students explore through questioning.",
                    learning_objectives="Understand communication principles through discovery.",
                    difficulty_level="intermediate",
                    estimated_duration=45,
                    is_active=True
                )
                db.add(module)
                created_modules += 1
        
        db.commit()
        print(f"✅ Created {created_modules} sample modules")
        
        print("\n🎉 DEMO SETUP COMPLETE!")
        print("=" * 40)
        print("Demo Accounts:")
        print("  🎓 Student: student@demo.com / student123")
        print("  🧑‍🏫 Teacher: teacher@demo.com / teacher123")
        print("  ⚙️ Admin: admin@demo.com / admin123")
        print("  🔄 Universal: demo@harv.com / demo123")
        print("\nServer starting...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(setup_demo_data())
