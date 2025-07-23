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
