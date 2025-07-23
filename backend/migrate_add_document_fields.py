#!/usr/bin/env python3
"""
REAL Database Migration - Add Document Intelligence Fields
This actually modifies your database structure
"""

import sqlite3
import os

def add_document_fields():
    """Add document intelligence fields to modules table"""
    
    db_path = "harv_v2.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 Adding document intelligence fields to modules table...")
        
        # Add all the new document intelligence fields
        fields_to_add = [
            ("source_document_path", "TEXT"),
            ("source_document_name", "TEXT"), 
            ("source_document_type", "TEXT"),
            ("document_processed_at", "DATETIME"),
            ("extracted_concepts", "TEXT"),
            ("extracted_examples", "TEXT"),
            ("socratic_questions", "TEXT"),
            ("document_summary", "TEXT")
        ]
        
        for field_name, field_type in fields_to_add:
            try:
                sql = f"ALTER TABLE modules ADD COLUMN {field_name} {field_type}"
                cursor.execute(sql)
                print(f"✅ Added field: {field_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️ Field already exists: {field_name}")
                else:
                    raise
        
        conn.commit()
        conn.close()
        
        print("🎉 Database migration complete!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = add_document_fields()
    if not success:
        exit(1)
