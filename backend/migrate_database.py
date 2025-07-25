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
