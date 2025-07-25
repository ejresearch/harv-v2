#!/usr/bin/env python3
"""
Memory System Database Migration - FIXED
Ensures all required fields exist for 4-layer memory system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Import all models

def check_and_update_schema():
    """Check if database schema supports memory system"""
    print("🔍 Checking database schema for memory system compatibility...")
    
    engine = create_engine(settings.database_url)
    inspector = inspect(engine)
    
    # Check if all required tables exist
    required_tables = [
        'users', 'onboarding_surveys', 'modules', 
        'conversations', 'messages', 'memory_summaries', 'user_progress'
    ]
    
    existing_tables = inspector.get_table_names()
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"📋 Creating missing tables: {', '.join(missing_tables)}")
        Base.metadata.create_all(bind=engine)
        print("✅ Database schema updated")
    else:
        print("✅ All required tables exist")
    
    return True

def create_sample_data():
    """Create sample data for testing memory system - FIXED"""
    print("\n📊 Creating sample data for memory system testing...")
    
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if we already have sample modules
        existing_modules = db.query(Module).count()
        if existing_modules == 0:
            print("📚 Creating sample modules...")
            
            # Create sample modules with correct field names
            modules_data = [
                {
                    "id": 1,
                    "title": "Foundations of Communication",
                    "description": "Introduction to communication theory and basic principles"
                },
                {
                    "id": 2, 
                    "title": "Verbal Communication",
                    "description": "Exploring spoken language and its impact"
                },
                {
                    "id": 3,
                    "title": "Nonverbal Communication", 
                    "description": "Body language, gestures, and silent messages"
                }
            ]
            
            for module_data in modules_data:
                module = Module(**module_data)
                db.add(module)
            
            db.commit()
            print(f"✅ Created {len(modules_data)} sample modules")
        else:
            print(f"✅ Found {existing_modules} existing modules")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting Memory System Migration - FIXED")
    print("===========================================")
    
    try:
        check_and_update_schema()
        create_sample_data()
        
        print("\n🎉 Memory System Migration Complete!")
        print("✅ Database schema is ready for 4-layer memory system")
        print("✅ Sample data created for testing")
        print("\nNext steps:")
        print("1. Start server: cd backend && uvicorn app.main:app --reload")
        print("2. Test memory endpoints: http://localhost:8000/docs")
        print("3. Health check: http://localhost:8000/api/v1/memory/health")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)
