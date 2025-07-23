#!/bin/bash
# Step 2: Run this script to add document intelligence fields to your database

echo "🗄️ Adding Document Intelligence to Database"
echo "============================================"

cd backend

# Create the migration file
cat > add_document_intelligence.py << 'EOF'
#!/usr/bin/env python3
"""
Add Document Intelligence to Modules Table
Adds the new fields for universal document diffusion
"""

import sqlite3
import os
from datetime import datetime

def add_document_intelligence_fields():
    """Add document intelligence fields to modules table"""
    
    # Connect to your existing database
    db_path = "harv_v2.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("📊 Adding document intelligence fields to modules table...")
        
        # Add all the new document intelligence fields
        migrations = [
            "ALTER TABLE modules ADD COLUMN source_document_path TEXT",
            "ALTER TABLE modules ADD COLUMN source_document_name TEXT", 
            "ALTER TABLE modules ADD COLUMN source_document_type TEXT",
            "ALTER TABLE modules ADD COLUMN document_processed_at DATETIME",
            "ALTER TABLE modules ADD COLUMN extracted_concepts TEXT",
            "ALTER TABLE modules ADD COLUMN extracted_examples TEXT",
            "ALTER TABLE modules ADD COLUMN socratic_questions TEXT",
            "ALTER TABLE modules ADD COLUMN document_summary TEXT"
        ]
        
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✅ Added: {migration.split('ADD COLUMN')[1].split()[0]}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e).lower():
                    print(f"⚠️ Field already exists: {migration.split('ADD COLUMN')[1].split()[0]}")
                else:
                    print(f"❌ Error with migration: {e}")
                    raise
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Document intelligence fields added successfully!")
        print("Your modules table is now ready for document uploads")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = add_document_intelligence_fields()
    if success:
        print("\n✅ Database migration complete - ready for document diffusion!")
    else:
        print("\n❌ Migration failed - check the error messages above")
EOF

# Run the migration
echo "🔄 Running database migration..."
python add_document_intelligence.py

if [[ $? -eq 0 ]]; then
    echo ""
    echo "✅ Database migration successful!"
    echo "Your modules table now supports document intelligence for all 15 modules"
else
    echo ""
    echo "❌ Migration failed - check the output above"
    exit 1
fi
