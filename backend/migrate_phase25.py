#!/usr/bin/env python3
"""
Phase 2.5 Database Migration
Adds tables and indexes for OpenAI integration and analytics
"""

import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_phase25_migration():
    """Run Phase 2.5 database migration"""
    
    try:
        # Connect to database
        conn = sqlite3.connect('harv_v2.db')
        cursor = conn.cursor()
        
        logger.info("🗄️ Starting Phase 2.5 database migration...")
        
        # Add OpenAI integration tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS openai_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                conversation_id TEXT,
                module_id INTEGER,
                prompt_tokens INTEGER DEFAULT 0,
                completion_tokens INTEGER DEFAULT 0,
                total_tokens INTEGER DEFAULT 0,
                model_used TEXT,
                cost_estimate REAL DEFAULT 0.0,
                socratic_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Add WebSocket session tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS websocket_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                user_id INTEGER,
                module_id INTEGER,
                connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                disconnected_at TIMESTAMP,
                message_count INTEGER DEFAULT 0,
                duration_seconds INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Add analytics tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                module_id INTEGER,
                metric_name TEXT,
                metric_value REAL,
                metric_unit TEXT,
                measurement_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Add indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_openai_usage_user_id ON openai_usage (user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_openai_usage_created_at ON openai_usage (created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_websocket_sessions_user_id ON websocket_sessions (user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_analytics_user_id ON learning_analytics (user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_analytics_date ON learning_analytics (measurement_date)')
        
        # Update existing tables with Phase 2.5 fields
        try:
            cursor.execute('ALTER TABLE conversation_history ADD COLUMN openai_model TEXT')
            cursor.execute('ALTER TABLE conversation_history ADD COLUMN token_usage INTEGER DEFAULT 0')
            cursor.execute('ALTER TABLE conversation_history ADD COLUMN cost_estimate REAL DEFAULT 0.0')
            logger.info("✅ Added Phase 2.5 fields to conversation_history")
        except sqlite3.OperationalError:
            logger.info("ℹ️ Phase 2.5 fields already exist in conversation_history")
        
        try:
            cursor.execute('ALTER TABLE memory_summaries ADD COLUMN context_optimization_score REAL DEFAULT 0.0')
            cursor.execute('ALTER TABLE memory_summaries ADD COLUMN personalization_score REAL DEFAULT 0.0')
            logger.info("✅ Added Phase 2.5 fields to memory_summaries")
        except sqlite3.OperationalError:
            logger.info("ℹ️ Phase 2.5 fields already exist in memory_summaries")
        
        # Commit changes
        conn.commit()
        
        logger.info("✅ Phase 2.5 database migration completed successfully")
        
        # Verify migration
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        logger.info(f"📊 Database now has {len(tables)} tables")
        
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_phase25_migration()
    if success:
        print("🎉 Phase 2.5 migration completed successfully!")
    else:
        print("❌ Migration failed!")
        exit(1)
