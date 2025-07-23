#!/bin/bash
# ACTUAL IMPLEMENTATION - The Real Work

echo "🔧 REAL IMPLEMENTATION STEPS"
echo "============================"
echo ""
echo "You're right to be suspicious! The previous script just prepared files."
echo "Here's the ACTUAL implementation work:"
echo ""

# Step 1: Database Migration (REAL)
echo "📊 Step 1: Database Migration (REQUIRED)"
echo "----------------------------------------"

cat > backend/migrate_add_document_fields.py << 'EOF'
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
EOF

echo "✅ Created REAL database migration script"

# Step 2: Module Model Enhancement (REAL)
echo ""
echo "📝 Step 2: Module Model Enhancement (REQUIRED)"
echo "----------------------------------------------"

cat > backend/temp_module_fields_to_add.py << 'EOF'
"""
ADD THESE FIELDS TO YOUR backend/app/models/course.py Module class

Find your existing Module class and add these imports at the top:
"""

# Add these imports to the TOP of your course.py file:
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime  # Add DateTime
from typing import Dict, List  # Add these
from datetime import datetime  # Add this
import json  # Add this

# Then add these fields to your existing Module class:
class Module(Base, TimestampMixin):
    # ... ALL YOUR EXISTING FIELDS ...
    
    # NEW: Add these fields at the end of your existing fields
    source_document_path = Column(String, nullable=True)
    source_document_name = Column(String, nullable=True)
    source_document_type = Column(String, nullable=True)
    document_processed_at = Column(DateTime, nullable=True)
    extracted_concepts = Column(Text, nullable=True)
    extracted_examples = Column(Text, nullable=True)
    socratic_questions = Column(Text, nullable=True)
    document_summary = Column(Text, nullable=True)
    
    # NEW: Add these methods at the end of your Module class
    def has_document_intelligence(self) -> bool:
        """Check if this module has document intelligence available"""
        return bool(self.extracted_concepts and self.extracted_examples)
    
    def get_document_concepts(self) -> Dict[str, str]:
        """Get extracted concepts as dictionary"""
        if not self.extracted_concepts:
            return {}
        try:
            return json.loads(self.extracted_concepts)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_document_examples(self) -> Dict[str, str]:
        """Get extracted examples as dictionary"""
        if not self.extracted_examples:
            return {}
        try:
            return json.loads(self.extracted_examples)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def get_socratic_questions(self) -> Dict[str, List[str]]:
        """Get generated Socratic questions as dictionary"""
        if not self.socratic_questions:
            return {"concept_questions": [], "application_questions": []}
        try:
            return json.loads(self.socratic_questions)
        except (json.JSONDecodeError, TypeError):
            return {"concept_questions": [], "application_questions": []}
    
    def get_document_status(self) -> Dict[str, any]:
        """Get complete document intelligence status"""
        return {
            "has_document": self.has_document_intelligence(),
            "document_name": self.source_document_name,
            "document_type": self.source_document_type,
            "processed_at": self.document_processed_at.isoformat() if self.document_processed_at else None,
            "concepts_count": len(self.get_document_concepts()),
            "examples_count": len(self.get_document_examples()),
            "questions_available": bool(self.socratic_questions)
        }

# MANUAL STEP: You need to manually add these to your actual course.py file
EOF

echo "✅ Created module enhancement code"
echo "⚠️  MANUAL STEP REQUIRED: Edit backend/app/models/course.py"

# Step 3: Document Processor Service (REAL)
echo ""
echo "🤖 Step 3: Document Processor Service (REQUIRED)"
echo "------------------------------------------------"

# This creates the actual service file
cat > backend/app/services/document_processor.py << 'EOF'
"""
Universal Document Processing Service - REAL IMPLEMENTATION
Transforms uploaded documents into module intelligence
"""

import json
import logging
import os
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import openai
from sqlalchemy.orm import Session

from app.models.course import Module
from app.core.config import settings

logger = logging.getLogger(__name__)

class UniversalDocumentProcessor:
    """Document processor that works with all 15 modules"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.supported_extensions = {'.pdf', '.docx', '.pptx', '.txt'}
    
    async def process_document_for_module(self, 
                                        file_path: str, 
                                        module_id: int, 
                                        db_session: Session,
                                        original_filename: Optional[str] = None) -> Dict[str, Any]:
        """Main processing method"""
        
        result = {
            "success": False,
            "module_id": module_id,
            "filename": original_filename or Path(file_path).name,
            "error": None,
            "processing_details": {}
        }
        
        try:
            logger.info(f"📄 Processing document for Module {module_id}: {file_path}")
            
            # Get the target module
            module = db_session.query(Module).filter(Module.id == module_id).first()
            if not module:
                result["error"] = f"Module {module_id} not found"
                return result
            
            # Extract content from document
            raw_content = await self._extract_document_content(file_path)
            if not raw_content:
                result["error"] = "No content could be extracted from document"
                return result
            
            result["processing_details"]["content_length"] = len(raw_content)
            
            # AI analysis using module context
            ai_analysis = await self._ai_analyze_content(raw_content, module)
            if not ai_analysis:
                result["error"] = "AI analysis failed"
                return result
            
            result["processing_details"]["ai_analysis"] = {
                "concepts_extracted": len(ai_analysis.get("key_concepts", {})),
                "examples_found": len(ai_analysis.get("real_world_examples", {})),
                "questions_generated": len(ai_analysis.get("socratic_questions", {}).get("concept_questions", []))
            }
            
            # Update module with intelligence
            update_success = await self._update_module_with_intelligence(
                module, ai_analysis, file_path, original_filename, db_session
            )
            
            if update_success:
                result["success"] = True
                result["message"] = f"Successfully enhanced Module {module_id} with document intelligence"
                logger.info(f"✅ Module {module_id} enhanced with document intelligence")
            else:
                result["error"] = "Failed to update module with extracted intelligence"
            
            return result
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            result["error"] = f"Processing failed: {str(e)}"
            return result
    
    async def _extract_document_content(self, file_path: str) -> Optional[str]:
        """Extract text content from document"""
        
        file_extension = Path(file_path).suffix.lower()
        
        try:
            if file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            else:
                # For now, just handle TXT files (can add PDF/DOCX later)
                logger.warning(f"Only TXT files supported currently: {file_extension}")
                return None
                
        except Exception as e:
            logger.error(f"Content extraction failed for {file_path}: {e}")
            return None
    
    async def _ai_analyze_content(self, content: str, module: Module) -> Optional[Dict[str, Any]]:
        """Use AI to analyze document content"""
        
        analysis_prompt = f"""
        You are an expert educational content analyzer for an intelligent tutoring system.
        
        ANALYZE this educational document for Module {module.id}: "{module.title}"
        
        MODULE CONTEXT:
        - Title: {module.title}
        - Description: {module.description or 'Not provided'}
        - Learning Objectives: {module.learning_objectives or 'Not specified'}
        
        DOCUMENT CONTENT TO ANALYZE:
        {content[:8000]}
        
        Extract educational intelligence and respond with ONLY valid JSON:
        
        {{
            "key_concepts": {{
                "concept_1": "Clear definition",
                "concept_2": "Clear definition"
            }},
            "real_world_examples": {{
                "example_1": "Description of example from document",
                "example_2": "Description of example from document"
            }},
            "socratic_questions": {{
                "concept_questions": [
                    "Question that guides discovery",
                    "Another discovery question"
                ],
                "application_questions": [
                    "Application question",
                    "Connection question"
                ]
            }},
            "document_summary": "Brief summary of main content"
        }}
        
        Focus on making the AI tutor more knowledgeable about THIS specific course material.
        """
        
        try:
            response = await self.openai_client.chat.completions.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educational content analyzer. Respond ONLY with valid JSON."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis_text = response.choices[0].message.content.strip()
            
            # Clean up response
            if analysis_text.startswith("```json"):
                analysis_text = analysis_text[7:]
            if analysis_text.endswith("```"):
                analysis_text = analysis_text[:-3]
            
            return json.loads(analysis_text)
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    async def _update_module_with_intelligence(self, 
                                             module: Module, 
                                             ai_analysis: Dict[str, Any], 
                                             file_path: str,
                                             original_filename: Optional[str],
                                             db_session: Session) -> bool:
        """Update the module with extracted intelligence"""
        
        try:
            # Store file information
            module.source_document_path = file_path
            module.source_document_name = original_filename or Path(file_path).name
            module.source_document_type = Path(file_path).suffix.lower()[1:]
            module.document_processed_at = datetime.utcnow()
            
            # Store extracted intelligence
            module.extracted_concepts = json.dumps(ai_analysis.get('key_concepts', {}))
            module.extracted_examples = json.dumps(ai_analysis.get('real_world_examples', {}))
            module.socratic_questions = json.dumps(ai_analysis.get('socratic_questions', {}))
            module.document_summary = ai_analysis.get('document_summary', '')
            
            db_session.commit()
            logger.info(f"✅ Module {module.id} updated with document intelligence")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update module {module.id}: {e}")
            db_session.rollback()
            return False
EOF

echo "✅ Created REAL document processor service"

echo ""
echo "🎯 IMPLEMENTATION SUMMARY"
echo "========================"
echo ""
echo "Created REAL implementation files:"
echo "✅ backend/migrate_add_document_fields.py - Database migration"
echo "✅ backend/app/services/document_processor.py - AI processing service"  
echo "✅ backend/temp_module_fields_to_add.py - Code to add to Module class"
echo ""
echo "MANUAL STEPS REQUIRED:"
echo "1. Edit backend/app/models/course.py - add the fields from temp_module_fields_to_add.py"
echo "2. Run: cd backend && python migrate_add_document_fields.py"
echo "3. Test: cd backend && python test_real_module1.py"
echo ""
echo "🔍 Current Status Check:"
echo "Try running the test now to see what fails:"
echo "   cd backend && python test_real_module1.py"
echo ""
echo "This will show you exactly what still needs to be implemented!"
